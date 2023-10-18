def stitch(csp, min_classical_gap=2.0, max_graph_size=8):
    """Build a binary quadratic model with minimal energy levels at solutions to the specified constraint satisfaction
    problem.

    Args:
        csp (:obj:`.ConstraintSatisfactionProblem`):
            Constraint satisfaction problem.

        min_classical_gap (float, optional, default=2.0):
            Minimum energy gap from ground. Each constraint violated by the solution increases
            the energy level of the binary quadratic model by at least this much relative
            to ground energy.

        max_graph_size (int, optional, default=8):
            Maximum number of variables in the binary quadratic model that can be used to
            represent a single constraint.

    Returns:
        :class:`~dimod.BinaryQuadraticModel`

    Notes:
        For a `min_classical_gap` > 2 or constraints with more than two variables, requires
        access to factories from the penaltymodel_ ecosystem to construct the binary quadratic
        model.

    .. _penaltymodel: https://github.com/dwavesystems/penaltymodel

    Examples:
        This example creates a binary-valued constraint satisfaction problem
        with two constraints, :math:`a = b` and :math:`b \\ne c`, and builds
        a binary quadratic model with a minimum energy level of -2 such that
        each constraint violation by a solution adds the default minimum energy gap.

        >>> import dwavebinarycsp
        >>> import operator
        >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        >>> csp.add_constraint(operator.eq, ['a', 'b'])  # a == b
        >>> csp.add_constraint(operator.ne, ['b', 'c'])  # b != c
        >>> bqm = dwavebinarycsp.stitch(csp)
        >>> bqm.energy({'a': 0, 'b': 0, 'c': 1})  # satisfies csp
        -2.0
        >>> bqm.energy({'a': 0, 'b': 0, 'c': 0})  # violates one constraint
        0.0
        >>> bqm.energy({'a': 1, 'b': 0, 'c': 0}) # violates two constraints
        2.0

        This example creates a binary-valued constraint satisfaction problem
        with two constraints, :math:`a = b` and :math:`b \\ne c`, and builds
        a binary quadratic model with a minimum energy gap of 4.
        Note that in this case the conversion to binary quadratic model adds two
        ancillary variables that must be minimized over when solving.

        >>> import dwavebinarycsp
        >>> import operator
        >>> import itertools
        >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        >>> csp.add_constraint(operator.eq, ['a', 'b'])  # a == b
        >>> csp.add_constraint(operator.ne, ['b', 'c'])  # b != c
        >>> bqm = dwavebinarycsp.stitch(csp, min_classical_gap=4.0)
        >>> list(bqm)   # # doctest: +SKIP
        ['a', 'aux1', 'aux0', 'b', 'c']
        >>> min([bqm.energy({'a': 0, 'b': 0, 'c': 1, 'aux0': aux0, 'aux1': aux1}) for
        ... aux0, aux1 in list(itertools.product([0, 1], repeat=2))])  # satisfies csp
        -6.0
        >>> min([bqm.energy({'a': 0, 'b': 0, 'c': 0, 'aux0': aux0, 'aux1': aux1}) for
        ... aux0, aux1 in list(itertools.product([0, 1], repeat=2))])  # violates one constraint
        -2.0
        >>> min([bqm.energy({'a': 1, 'b': 0, 'c': 0, 'aux0': aux0, 'aux1': aux1}) for
        ... aux0, aux1 in list(itertools.product([0, 1], repeat=2))])  # violates two constraints
        2.0

        This example finds for the previous example the minimum graph size.

        >>> import dwavebinarycsp
        >>> import operator
        >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        >>> csp.add_constraint(operator.eq, ['a', 'b'])  # a == b
        >>> csp.add_constraint(operator.ne, ['b', 'c'])  # b != c
        >>> for n in range(8, 1, -1):
        ...     try:
        ...         bqm = dwavebinarycsp.stitch(csp, min_classical_gap=4.0, max_graph_size=n)
        ...     except dwavebinarycsp.exceptions.ImpossibleBQM:
        ...         print(n+1)
        ...
        3

    """

    # ensure we have penaltymodel factory available
    try:
        dwavebinarycsp.assert_penaltymodel_factory_available()
    except AssertionError as e:
        raise RuntimeError(e)

    def aux_factory():
        for i in count():
            yield 'aux{}'.format(i)

    aux = aux_factory()

    bqm = dimod.BinaryQuadraticModel.empty(csp.vartype)

    # developer note: we could cache them and relabel, for now though let's do the simple thing
    # penalty_models = {}
    for const in csp.constraints:
        configurations = const.configurations

        if len(const.variables) > max_graph_size:
            msg = ("The given csp contains a constraint {const} with {num_var} variables. "
                   "This cannot be mapped to a graph with {max_graph_size} nodes. "
                   "Consider checking whether your constraint is irreducible."
                   "").format(const=const, num_var=len(const.variables), max_graph_size=max_graph_size)
            raise ImpossibleBQM(msg)

        pmodel = None

        if len(const) == 0:
            # empty constraint
            continue

        if min_classical_gap <= 2.0:
            if len(const) == 1 and max_graph_size >= 1:
                bqm.update(_bqm_from_1sat(const))
                continue
            elif len(const) == 2 and max_graph_size >= 2:
                bqm.update(_bqm_from_2sat(const))
                continue

        # developer note: we could cache them and relabel, for now though let's do the simple thing
        # if configurations in penalty_models:
        #     raise NotImplementedError

        for G in iter_complete_graphs(const.variables, max_graph_size + 1, aux):

            # construct a specification
            spec = pm.Specification(
                graph=G,
                decision_variables=const.variables,
                feasible_configurations=configurations,
                min_classical_gap=min_classical_gap,
                vartype=csp.vartype
            )

            # try to use the penaltymodel ecosystem
            try:
                pmodel = pm.get_penalty_model(spec)
            except pm.ImpossiblePenaltyModel:
                # hopefully adding more variables will make it possible
                continue

            if pmodel.classical_gap >= min_classical_gap:
                break

        # developer note: we could cache them and relabel, for now though let's do the simple thing
        # penalty_models[configurations] = pmodel

        else:
            msg = ("No penalty model can be build for constraint {}".format(const))
            raise ImpossibleBQM(msg)

        bqm.update(pmodel.model)

    return bqm