def __check_parameters(self):
        """!
        @brief Checks input parameters of the algorithm and if something wrong then corresponding exception is thrown.

        """
        if (self.__amount <= 0) or (self.__amount > len(self.__data)):
            raise AttributeError("Amount of cluster centers '" + str(self.__amount) + "' should be at least 1 and "
                                 "should be less or equal to amount of points in data.")

        if self.__candidates != kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE:
            if (self.__candidates <= 0) or (self.__candidates > len(self.__data)):
                raise AttributeError("Amount of center candidates '" + str(self.__candidates) + "' should be at least 1 "
                                     "and should be less or equal to amount of points in data.")

        if len(self.__data) == 0:
            raise AttributeError("Data is empty.")