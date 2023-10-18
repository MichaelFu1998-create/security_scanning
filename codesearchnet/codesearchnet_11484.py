def from_func(cls, func, variables, vartype, name=None):
        """Construct a constraint from a validation function.

        Args:
            func (function):
                Function that evaluates True when the variables satisfy the constraint.

            variables (iterable):
                Iterable of variable labels.

            vartype (:class:`~dimod.Vartype`/str/set):
                Variable type for the constraint. Accepted input values:

                * :attr:`~dimod.Vartype.SPIN`, ``'SPIN'``, ``{-1, 1}``
                * :attr:`~dimod.Vartype.BINARY`, ``'BINARY'``, ``{0, 1}``

            name (string, optional, default='Constraint'):
                Name for the constraint.

        Examples:
            This example creates a constraint that binary variables `a` and `b`
            are not equal.

            >>> import dwavebinarycsp
            >>> import operator
            >>> const = dwavebinarycsp.Constraint.from_func(operator.ne, ['a', 'b'], 'BINARY')
            >>> print(const.name)
            Constraint
            >>> (0, 1) in const.configurations
            True

            This example creates a constraint that :math:`out = NOT(x)`
            for spin variables.

            >>> import dwavebinarycsp
            >>> def not_(y, x):  # y=NOT(x) for spin variables
            ...     return (y == -x)
            ...
            >>> const = dwavebinarycsp.Constraint.from_func(
            ...               not_,
            ...               ['out', 'in'],
            ...               {1, -1},
            ...               name='not_spin')
            >>> print(const.name)
            not_spin
            >>> (1, -1) in const.configurations
            True

        """
        variables = tuple(variables)

        configurations = frozenset(config
                                   for config in itertools.product(vartype.value, repeat=len(variables))
                                   if func(*config))

        return cls(func, configurations, variables, vartype, name)