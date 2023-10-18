def projection(self, variables):
        """Create a new constraint that is the projection onto a subset of the variables.

        Args:
            variables (iterable):
                Subset of the constraint's variables.

        Returns:
            :obj:`.Constraint`: A new constraint over a subset of the variables.

        Examples:

            >>> import dwavebinarycsp
            ...
            >>> const = dwavebinarycsp.Constraint.from_configurations([(0, 0), (0, 1)],
            ...                                                       ['a', 'b'],
            ...                                                       dwavebinarycsp.BINARY)
            >>> proj = const.projection(['a'])
            >>> proj.variables
            ['a']
            >>> proj.configurations
            {(0,)}

        """
        # resolve iterables or mutability problems by casting the variables to a set
        variables = set(variables)

        if not variables.issubset(self.variables):
            raise ValueError("Cannot project to variables not in the constraint.")

        idxs = [i for i, v in enumerate(self.variables) if v in variables]

        configurations = frozenset(tuple(config[i] for i in idxs) for config in self.configurations)
        variables = tuple(self.variables[i] for i in idxs)

        return self.from_configurations(configurations, variables, self.vartype)