def flip_variable(self, v):
        """Flip a variable in the constraint.

        Args:
            v (variable):
                Variable in the constraint to take the complementary value of its
                construction value.

        Examples:
            This example creates a constraint that :math:`a = b` on binary variables
            and flips variable a.

            >>> import dwavebinarycsp
            >>> const = dwavebinarycsp.Constraint.from_func(operator.eq,
            ...             ['a', 'b'], dwavebinarycsp.BINARY)
            >>> const.check({'a': 0, 'b': 0})
            True
            >>> const.flip_variable('a')
            >>> const.check({'a': 1, 'b': 0})
            True
            >>> const.check({'a': 0, 'b': 0})
            False

        """
        try:
            idx = self.variables.index(v)
        except ValueError:
            raise ValueError("variable {} is not a variable in constraint {}".format(v, self.name))

        if self.vartype is dimod.BINARY:

            original_func = self.func

            def func(*args):
                new_args = list(args)
                new_args[idx] = 1 - new_args[idx]  # negate v
                return original_func(*new_args)

            self.func = func

            self.configurations = frozenset(config[:idx] + (1 - config[idx],) + config[idx + 1:]
                                            for config in self.configurations)

        else:  # SPIN

            original_func = self.func

            def func(*args):
                new_args = list(args)
                new_args[idx] = -new_args[idx]  # negate v
                return original_func(*new_args)

            self.func = func

            self.configurations = frozenset(config[:idx] + (-config[idx],) + config[idx + 1:]
                                            for config in self.configurations)

        self.name = '{} ({} flipped)'.format(self.name, v)