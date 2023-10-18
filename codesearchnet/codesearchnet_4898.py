def __validate_arguments(self):
        """!
        @brief Check input arguments of BANG algorithm and if one of them is not correct then appropriate exception
                is thrown.

        """
        if self.__levels <= 0:
            raise ValueError("Incorrect amount of levels '%d'. Level value should be greater than 0." % self.__levels)

        if len(self.__data) == 0:
            raise ValueError("Empty input data. Data should contain at least one point.")

        if self.__density_threshold < 0:
            raise ValueError("Incorrect density threshold '%f'. Density threshold should not be negative." % self.__density_threshold)