def __process_by_ccore(self):
        """!
        @brief Performs cluster analysis using C/C++ implementation.

        """
        result = wrapper.fcm_algorithm(self.__data, self.__centers, self.__m, self.__tolerance, self.__itermax)

        self.__clusters = result[wrapper.fcm_package_indexer.INDEX_CLUSTERS]
        self.__centers = result[wrapper.fcm_package_indexer.INDEX_CENTERS]
        self.__membership = result[wrapper.fcm_package_indexer.INDEX_MEMBERSHIP]