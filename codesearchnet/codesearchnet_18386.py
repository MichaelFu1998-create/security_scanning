def _add_positional_argument(self, posarg):
        """Append a positional argument to the user interface.

        Optional positional arguments must be added after the required ones. 
        The user interface can have at most one recurring positional argument, 
        and if present, that argument must be the last one.
        """
        if self.positional_args:
            if self.positional_args[-1].recurring:
                raise ValueError("recurring positional arguments must be last")
            if self.positional_args[-1].optional and not posarg.optional:
                raise ValueError("required positional arguments must precede optional ones")
        self.positional_args.append(posarg)