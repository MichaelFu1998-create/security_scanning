def __caclulate_optimal_neighbor_cluster_score(self, index_cluster, difference):
        """!
        @brief Calculates 'B' score for the specific object for the nearest cluster.

        @param[in] index_point (uint): Index point from input data for which 'B' score should be calculated.
        @param[in] index_cluster (uint): Index cluster to which the point is belong to.

        @return (float) 'B' score for the object.

        """

        optimal_score = float('inf')
        for index_neighbor_cluster in range(len(self.__clusters)):
            if index_cluster != index_neighbor_cluster:
                candidate_score = self.__calculate_cluster_score(index_neighbor_cluster, difference)
                if candidate_score < optimal_score:
                    optimal_score = candidate_score

        if optimal_score == float('inf'):
            optimal_score = -1.0

        return optimal_score