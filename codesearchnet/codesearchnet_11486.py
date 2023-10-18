def check(self, solution):
        """Check that a solution satisfies the constraint.

        Args:
            solution (container):
                An assignment for the variables in the constraint.

        Returns:
            bool: True if the solution satisfies the constraint; otherwise False.

        Examples:
            This example creates a constraint that :math:`a \\ne b` on binary variables
            and tests it for two candidate solutions, with additional unconstrained
            variable c.

            >>> import dwavebinarycsp
            >>> const = dwavebinarycsp.Constraint.from_configurations([(0, 1), (1, 0)],
            ...             ['a', 'b'], dwavebinarycsp.BINARY)
            >>> solution = {'a': 1, 'b': 1, 'c': 0}
            >>> const.check(solution)
            False
            >>> solution = {'a': 1, 'b': 0, 'c': 0}
            >>> const.check(solution)
            True

        """
        return self.func(*(solution[v] for v in self.variables))