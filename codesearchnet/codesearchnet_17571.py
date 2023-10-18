def _is_size_class_mass_tuple(self, value):
        """
        Determines whether value is a tuple of the format
        (size class(float), mass(float)).

        :param value: The value to check.

        :returns: Whether the value is a tuple in the required format.
        """

        if not type(value) is tuple:
            return False
        elif not len(value) == 2:
            return False
        elif not type(value[0]) is float:
            return False
        elif not type(value[1]) is float and \
                not type(value[1]) is numpy.float64 and \
                not type(value[1]) is numpy.float32:
            return False
        else:
            return True