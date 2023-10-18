def __calculate_cluster_score(self, index_cluster, difference):
        """!
        @brief Calculates 'B*' score for the specific object for specific cluster.

        @param[in] index_point (uint): Index point from input data for which 'B*' score should be calculated.
        @param[in] index_cluster (uint): Index cluster to which the point is belong to.

        @return (float) 'B*' score for the object for specific cluster.

        """

        score = self.__calculate_cluster_difference(index_cluster, difference)
        return score / len(self.__clusters[index_cluster])