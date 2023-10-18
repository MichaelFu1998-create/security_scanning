def __calculate_within_cluster_score(self, index_cluster, difference):
        """!
        @brief Calculates 'A' score for the specific object in cluster to which it belongs to.

        @param[in] index_point (uint): Index point from input data for which 'A' score should be calculated.
        @param[in] index_cluster (uint): Index cluster to which the point is belong to.

        @return (float) 'A' score for the object.

        """

        score = self.__calculate_cluster_difference(index_cluster, difference)
        if len(self.__clusters[index_cluster]) == 1:
            return float('nan')
        return score / (len(self.__clusters[index_cluster]) - 1)