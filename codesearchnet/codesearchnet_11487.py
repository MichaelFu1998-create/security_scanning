def fix_variable(self, v, value):
        """Fix the value of a variable and remove it from the constraint.

        Args:
            v (variable):
                Variable in the constraint to be set to a constant value.

            val (int):
                Value assigned to the variable. Values must match the :class:`.Vartype` of the
                constraint.

        Examples:
            This example creates a constraint that :math:`a \\ne b` on binary variables,
            fixes variable a to 0, and tests two candidate solutions.

            >>> import dwavebinarycsp
            >>> const = dwavebinarycsp.Constraint.from_func(operator.ne,
            ...             ['a', 'b'], dwavebinarycsp.BINARY)
            >>> const.fix_variable('a', 0)
            >>> const.check({'b': 1})
            True
            >>> const.check({'b': 0})
            False

        """
        variables = self.variables
        try:
            idx = variables.index(v)
        except ValueError:
            raise ValueError("given variable {} is not part of the constraint".format(v))

        if value not in self.vartype.value:
            raise ValueError("expected value to be in {}, received {} instead".format(self.vartype.value, value))

        configurations = frozenset(config[:idx] + config[idx + 1:]  # exclude the fixed var
                                   for config in self.configurations
                                   if config[idx] == value)

        if not configurations:
            raise UnsatError("fixing {} to {} makes this constraint unsatisfiable".format(v, value))

        variables = variables[:idx] + variables[idx + 1:]

        self.configurations = configurations
        self.variables = variables

        def func(*args): return args in configurations
        self.func = func

        self.name = '{} ({} fixed to {})'.format(self.name, v, value)