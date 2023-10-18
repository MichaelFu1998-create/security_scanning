def __calculate_score(self, index_point, index_cluster):
        """!
        @brief Calculates Silhouette score for the specific object defined by index_point.

        @param[in] index_point (uint): Index point from input data for which Silhouette score should be calculated.
        @param[in] index_cluster (uint): Index cluster to which the point belongs to.

        @return (float) Silhouette score for the object.

        """
        difference = self.__calculate_dataset_difference(index_point)

        a_score = self.__calculate_within_cluster_score(index_cluster, difference)
        b_score = self.__caclulate_optimal_neighbor_cluster_score(index_cluster, difference)

        return (b_score - a_score) / max(a_score, b_score)