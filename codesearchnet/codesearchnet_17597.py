def _is_compound_mass_tuple(self, value):
        """
        Determines whether value is a tuple of the format
        (compound(str), mass(float)).

        :param value: The value to be tested.

        :returns: True or False
        """

        if not type(value) is tuple:
            return False
        elif not len(value) == 2:
            return False
        elif not type(value[0]) is str:
            return False
        elif not type(value[1]) is float and \
                not type(value[1]) is numpy.float64 and \
                not type(value[1]) is numpy.float32:
            return False
        else:
            return True