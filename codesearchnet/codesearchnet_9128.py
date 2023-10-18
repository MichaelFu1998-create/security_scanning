def _check_input(self, input):
        """Checks the validity of the input.

        In case of an invalid input throws ValueError.
        """
        if isinstance(input, str):
            return 'st'
        elif isinstance(input, list):
            if all(isinstance(item, str) for item in input):
                return 'gst'

        raise ValueError("String argument should be of type String or"
                                     " a list of strings")