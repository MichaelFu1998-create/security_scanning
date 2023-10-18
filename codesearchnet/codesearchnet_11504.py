def fulladder_gate(variables, vartype=dimod.BINARY, name='FULL_ADDER'):
    """Full adder.

    Args:
        variables (list): Variable labels for the and gate as `[in1, in2, in3, sum, carry]`,
            where `in1, in2, in3` are inputs to be added and `sum` and 'carry' the resultant
            outputs.
        vartype (Vartype, optional, default='BINARY'): Variable type. Accepted
            input values:

            * Vartype.SPIN, 'SPIN', {-1, 1}
            * Vartype.BINARY, 'BINARY', {0, 1}
        name (str, optional, default='FULL_ADDER'): Name for the constraint.

    Returns:
        Constraint(:obj:`.Constraint`): Constraint that is satisfied when its variables are
        assigned values that match the valid states of a Boolean full adder.

    Examples:
        >>> import dwavebinarycsp
        >>> import dwavebinarycsp.factories.constraint.gates as gates
        >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        >>> csp.add_constraint(gates.fulladder_gate(['a', 'b', 'c_in', 'total', 'c_out'], name='FA1'))
        >>> csp.check({'a': 1, 'b': 0, 'c_in': 1, 'total': 0, 'c_out': 1})
        True

    """

    variables = tuple(variables)

    if vartype is dimod.BINARY:
        configs = frozenset([(0, 0, 0, 0, 0),
                             (0, 0, 1, 1, 0),
                             (0, 1, 0, 1, 0),
                             (0, 1, 1, 0, 1),
                             (1, 0, 0, 1, 0),
                             (1, 0, 1, 0, 1),
                             (1, 1, 0, 0, 1),
                             (1, 1, 1, 1, 1)])

    else:
        # SPIN, vartype is checked by the decorator
        configs = frozenset([(-1, -1, -1, -1, -1),
                             (-1, -1, +1, +1, -1),
                             (-1, +1, -1, +1, -1),
                             (-1, +1, +1, -1, +1),
                             (+1, -1, -1, +1, -1),
                             (+1, -1, +1, -1, +1),
                             (+1, +1, -1, -1, +1),
                             (+1, +1, +1, +1, +1)])

    def func(in1, in2, in3, sum_, carry):
        total = (in1 > 0) + (in2 > 0) + (in3 > 0)
        if total == 0:
            return (sum_ <= 0) and (carry <= 0)
        elif total == 1:
            return (sum_ > 0) and (carry <= 0)
        elif total == 2:
            return (sum_ <= 0) and (carry > 0)
        elif total == 3:
            return (sum_ > 0) and (carry > 0)
        else:
            raise ValueError("func recieved unexpected values")

    return Constraint(func, configs, variables, vartype=vartype, name=name)