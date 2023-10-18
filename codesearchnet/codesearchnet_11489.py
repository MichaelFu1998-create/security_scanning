def copy(self):
        """Create a copy.

        Examples:
            This example copies constraint :math:`a \\ne b` and tests a solution
            on the copied constraint.

            >>> import dwavebinarycsp
            >>> import operator
            >>> const = dwavebinarycsp.Constraint.from_func(operator.ne,
            ...             ['a', 'b'], 'BINARY')
            >>> const2 = const.copy()
            >>> const2 is const
            False
            >>> const2.check({'a': 1, 'b': 1})
            False

        """
        # each object is itself immutable (except the function)
        return self.__class__(self.func, self.configurations, self.variables, self.vartype, name=self.name)