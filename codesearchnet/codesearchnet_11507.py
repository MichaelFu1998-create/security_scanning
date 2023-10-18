def random_xorsat(num_variables, num_clauses, vartype=dimod.BINARY, satisfiable=True):
    """Random XOR constraint satisfaction problem.

    Args:
        num_variables (integer): Number of variables (at least three).
        num_clauses (integer): Number of constraints that together constitute the
            constraint satisfaction problem.
        vartype (Vartype, optional, default='BINARY'): Variable type. Accepted
            input values:

            * Vartype.SPIN, 'SPIN', {-1, 1}
            * Vartype.BINARY, 'BINARY', {0, 1}
        satisfiable (bool, optional, default=True): True if the CSP can be satisfied.

    Returns:
        CSP (:obj:`.ConstraintSatisfactionProblem`): CSP that is satisfied when its variables
        are assigned values that satisfy a XOR satisfiability problem.

    Examples:
        This example creates a CSP with 5 variables and two random constraints and checks
        whether a particular assignment of variables satisifies it.

        >>> import dwavebinarycsp
        >>> import dwavebinarycsp.factories as sat
        >>> csp = sat.random_xorsat(5, 2)
        >>> csp.constraints    # doctest: +SKIP
        [Constraint.from_configurations(frozenset({(1, 0, 0), (1, 1, 1), (0, 1, 0), (0, 0, 1)}), (4, 3, 0),
         Vartype.BINARY, name='XOR (0 flipped)'),
         Constraint.from_configurations(frozenset({(1, 1, 0), (0, 1, 1), (0, 0, 0), (1, 0, 1)}), (2, 0, 4),
         Vartype.BINARY, name='XOR (2 flipped) (0 flipped)')]
        >>> csp.check({0: 1, 1: 0, 2: 0, 3: 1, 4: 1})       # doctest: +SKIP
        True

    """
    if num_variables < 3:
        raise ValueError("a xor problem needs at least 3 variables")
    if num_clauses > 8 * _nchoosek(num_variables, 3):  # 8 different negation patterns
        raise ValueError("too many clauses")

    # also checks the vartype argument
    csp = ConstraintSatisfactionProblem(vartype)

    variables = list(range(num_variables))

    constraints = set()

    if satisfiable:
        values = tuple(vartype.value)
        planted_solution = {v: choice(values) for v in variables}

        configurations = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]

        while len(constraints) < num_clauses:
            # because constraints are hashed on configurations/variables, and because the inputs
            # to xor can be swapped without loss of generality, we can order them
            x, y, z = sample(variables, 3)
            if y > x:
                x, y = y, x

            # get the constraint
            const = xor_gate([x, y, z], vartype=vartype)

            # pick (uniformly) a configuration and determine which variables we need to negate to
            # match the chosen configuration
            config = choice(configurations)

            for idx, v in enumerate(const.variables):
                if config[idx] != (planted_solution[v] > 0):
                    const.flip_variable(v)

            assert const.check(planted_solution)

            constraints.add(const)
    else:
        while len(constraints) < num_clauses:
            # because constraints are hashed on configurations/variables, and because the inputs
            # to xor can be swapped without loss of generality, we can order them
            x, y, z = sample(variables, 3)
            if y > x:
                x, y = y, x

            # get the constraint
            const = xor_gate([x, y, z], vartype=vartype)

            # randomly flip each variable in the constraint
            for idx, v in enumerate(const.variables):
                if random() > .5:
                    const.flip_variable(v)

            assert const.check(planted_solution)

            constraints.add(const)

    for const in constraints:
        csp.add_constraint(const)

    # in case any variables didn't make it in
    for v in variables:
        csp.add_variable(v)

    return csp