def __process_by_ccore(self):
        """!
        @brief Performs processing using C++ implementation.

        """
        if isinstance(self.__initializer, kmeans_plusplus_initializer):
            initializer = wrapper.elbow_center_initializer.KMEANS_PLUS_PLUS
        else:
            initializer = wrapper.elbow_center_initializer.RANDOM

        result = wrapper.elbow(self.__data, self.__kmin, self.__kmax, initializer)

        self.__kvalue = result[0]
        self.__wce = result[1]