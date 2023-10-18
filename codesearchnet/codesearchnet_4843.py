def __validate_arguments(self):
        """!
        @brief Check input arguments of CLIQUE algorithm and if one of them is not correct then appropriate exception
                is thrown.

        """

        if len(self.__data) == 0:
            raise ValueError("Empty input data. Data should contain at least one point.")

        if self.__amount_intervals <= 0:
            raise ValueError("Incorrect amount of intervals '%d'. Amount of intervals value should be greater than 0." % self.__amount_intervals)

        if self.__density_threshold < 0:
            raise ValueError("Incorrect density threshold '%f'. Density threshold should not be negative." % self.__density_threshold)