def get_operator(self, op):
        """Assigns function to the operators property of the instance.
        """
        if op in self.OPERATORS:
            return self.OPERATORS.get(op)
        try:
            n_args = len(inspect.getargspec(op)[0])
            if n_args != 2:
                raise TypeError
        except:
            eprint('Error: invalid operator function. Operators must accept two args.')
            raise
        else:
            return op