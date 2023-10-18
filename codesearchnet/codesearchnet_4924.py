def __verify_arguments(self):
        """!
        @brief Checks algorithm's arguments and if some of them is incorrect then exception is thrown.

        """
        if self.__kmax > len(self.__data):
            raise ValueError("K max value '" + str(self.__kmax) + "' is bigger than amount of objects '" +
                             str(len(self.__data)) + "' in input data.")

        if self.__kmin <= 1:
            raise ValueError("K min value '" + str(self.__kmin) + "' should be greater than 1 (impossible to provide "
                             "silhouette score for only one cluster).")