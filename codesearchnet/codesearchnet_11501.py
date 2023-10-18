def and_gate(variables, vartype=dimod.BINARY, name='AND'):
    """AND gate.

    Args:
        variables (list): Variable labels for the and gate as `[in1, in2, out]`,
            where `in1, in2` are inputs and `out` the gate's output.
        vartype (Vartype, optional, default='BINARY'): Variable type. Accepted
            input values:

            * Vartype.SPIN, 'SPIN', {-1, 1}
            * Vartype.BINARY, 'BINARY', {0, 1}
        name (str, optional, default='AND'): Name for the constraint.

    Returns:
        Constraint(:obj:`.Constraint`): Constraint that is satisfied when its variables are
        assigned values that match the valid states of an AND gate.

    Examples:
        >>> import dwavebinarycsp
        >>> import dwavebinarycsp.factories.constraint.gates as gates
        >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        >>> csp.add_constraint(gates.and_gate(['a', 'b', 'c'], name='AND1'))
        >>> csp.check({'a': 1, 'b': 0, 'c': 0})
        True
    """

    variables = tuple(variables)

    if vartype is dimod.BINARY:
        configurations = frozenset([(0, 0, 0),
                                    (0, 1, 0),
                                    (1, 0, 0),
                                    (1, 1, 1)])

        def func(in1, in2, out): return (in1 and in2) == out

    else:
        # SPIN, vartype is checked by the decorator
        configurations = frozenset([(-1, -1, -1),
                                    (-1, +1, -1),
                                    (+1, -1, -1),
                                    (+1, +1, +1)])

        def func(in1, in2, out): return ((in1 > 0) and (in2 > 0)) == (out > 0)

    return Constraint(func, configurations, variables, vartype=vartype, name=name)