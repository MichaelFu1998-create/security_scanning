def __calculate_cluster_difference(self, index_cluster, difference):
        """!
        @brief Calculates distance from each object in specified cluster to specified object.

        @param[in] index_point (uint): Index point for which difference is calculated.

        @return (list) Distance from specified object to each object from input data in specified cluster.

        """
        cluster_difference = 0.0
        for index_point in self.__clusters[index_cluster]:
            cluster_difference += difference[index_point]

        return cluster_difference