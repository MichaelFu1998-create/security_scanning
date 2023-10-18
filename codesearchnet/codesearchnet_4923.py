def __calculate_clusters(self, k):
        """!
        @brief Performs cluster analysis using specified K value.

        @param[in] k (uint): Amount of clusters that should be allocated.

        @return (array_like) Allocated clusters.

        """
        initial_values = kmeans_plusplus_initializer(self.__data, k).initialize(return_index=self.__return_index)
        algorithm_type = self.__algorithm.get_type()
        return algorithm_type(self.__data, initial_values).process().get_clusters()