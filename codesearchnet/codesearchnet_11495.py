def add_constraint(self, constraint, variables=tuple()):
        """Add a constraint.

        Args:
            constraint (function/iterable/:obj:`.Constraint`):
                Constraint definition in one of the supported formats:

                1. Function, with input arguments matching the order and
                   :attr:`~.ConstraintSatisfactionProblem.vartype` type of the `variables`
                   argument, that evaluates True when the constraint is satisfied.
                2. List explicitly specifying each allowed configuration as a tuple.
                3. :obj:`.Constraint` object built either explicitly or by :mod:`dwavebinarycsp.factories`.

            variables(iterable):
                Variables associated with the constraint. Not required when `constraint` is
                a :obj:`.Constraint` object.

        Examples:
            This example defines a function that evaluates True when the constraint is satisfied.
            The function's input arguments match the order and type of the `variables` argument.

            >>> import dwavebinarycsp
            >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
            >>> def all_equal(a, b, c):  # works for both dwavebinarycsp.BINARY and dwavebinarycsp.SPIN
            ...     return (a == b) and (b == c)
            >>> csp.add_constraint(all_equal, ['a', 'b', 'c'])
            >>> csp.check({'a': 0, 'b': 0, 'c': 0})
            True
            >>> csp.check({'a': 0, 'b': 0, 'c': 1})
            False

            This example explicitly lists allowed configurations.

            >>> import dwavebinarycsp
            >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.SPIN)
            >>> eq_configurations = {(-1, -1), (1, 1)}
            >>> csp.add_constraint(eq_configurations, ['v0', 'v1'])
            >>> csp.check({'v0': -1, 'v1': +1})
            False
            >>> csp.check({'v0': -1, 'v1': -1})
            True

            This example uses a :obj:`.Constraint` object built by :mod:`dwavebinarycsp.factories`.

            >>> import dwavebinarycsp
            >>> import dwavebinarycsp.factories.constraint.gates as gates
            >>> csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
            >>> csp.add_constraint(gates.and_gate(['a', 'b', 'c']))  # add an AND gate
            >>> csp.add_constraint(gates.xor_gate(['a', 'c', 'd']))  # add an XOR gate
            >>> csp.check({'a': 1, 'b': 0, 'c': 0, 'd': 1})
            True

        """
        if isinstance(constraint, Constraint):
            if variables and (tuple(variables) != constraint.variables):
                raise ValueError("mismatched variables and Constraint")
        elif isinstance(constraint, Callable):
            constraint = Constraint.from_func(constraint, variables, self.vartype)
        elif isinstance(constraint, Iterable):
            constraint = Constraint.from_configurations(constraint, variables, self.vartype)
        else:
            raise TypeError("Unknown constraint type given")

        self.constraints.append(constraint)
        for v in constraint.variables:
            self.variables[v].append(constraint)