def get_int_range_validator(start, stop):
        """Return an integer range validator to be used with `add_setting`.

        :Parameters:
            - `start`: minimum value for the integer
            - `stop`: the upper bound (maximum value + 1)
        :Types:
            - `start`: `int`
            - `stop`: `int`

        :return: a validator function
        """
        def validate_int_range(value):
            """Integer range validator."""
            value = int(value)
            if value >= start and value < stop:
                return value
            raise ValueError("Not in <{0},{1}) range".format(start, stop))
        return validate_int_range