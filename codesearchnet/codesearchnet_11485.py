def from_configurations(cls, configurations, variables, vartype, name=None):
        """Construct a constraint from valid configurations.

        Args:
            configurations (iterable[tuple]):
                Valid configurations of the variables. Each configuration is a tuple of variable
                assignments ordered by :attr:`~Constraint.variables`.

            variables (iterable):
                Iterable of variable labels.

            vartype (:class:`~dimod.Vartype`/str/set):
                Variable type for the constraint. Accepted input values:

                * :attr:`~dimod.Vartype.SPIN`, ``'SPIN'``, ``{-1, 1}``
                * :attr:`~dimod.Vartype.BINARY`, ``'BINARY'``, ``{0, 1}``

            name (string, optional, default='Constraint'):
                Name for the constraint.

        Examples:

            This example creates a constraint that variables `a` and `b` are not equal.

            >>> import dwavebinarycsp
            >>> const = dwavebinarycsp.Constraint.from_configurations([(0, 1), (1, 0)],
            ...                   ['a', 'b'], dwavebinarycsp.BINARY)
            >>> print(const.name)
            Constraint
            >>> (0, 0) in const.configurations   # Order matches variables: a,b
            False

            This example creates a constraint based on specified valid configurations
            that represents an OR gate for spin variables.

            >>> import dwavebinarycsp
            >>> const = dwavebinarycsp.Constraint.from_configurations(
            ...           [(-1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)],
            ...           ['y', 'x1', 'x2'],
            ...           dwavebinarycsp.SPIN, name='or_spin')
            >>> print(const.name)
            or_spin
            >>> (1, 1, -1) in const.configurations   # Order matches variables: y,x1,x2
            True

        """
        def func(*args): return args in configurations

        return cls(func, configurations, variables, vartype, name)