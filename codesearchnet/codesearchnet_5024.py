def __validate_arguments(self):
        """!
        @brief Check input arguments of BANG algorithm and if one of them is not correct then appropriate exception
                is thrown.

        """

        if len(self.__pointer_data) == 0:
            raise ValueError("Empty input data. Data should contain at least one point.")

        if self.__number_cluster <= 0:
            raise ValueError("Incorrect amount of clusters '%d'. Amount of cluster should be greater than 0." % self.__number_cluster)

        if self.__compression < 0:
            raise ValueError("Incorrect compression level '%f'. Compression should not be negative." % self.__compression)

        if self.__number_represent_points <= 0:
            raise ValueError("Incorrect amount of representatives '%d'. Amount of representatives should be greater than 0." % self.__number_cluster)