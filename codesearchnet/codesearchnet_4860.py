def _update_representative(self, index_cluster, point):
        """!
        @brief Update cluster representative in line with new cluster size and added point to it.

        @param[in] index_cluster (uint): Index of cluster whose representative should be updated.
        @param[in] point (list): Point that was added to cluster.

        """
        length = len(self._clusters[index_cluster]);
        rep = self._representatives[index_cluster];

        for dimension in range(len(rep)):
            rep[dimension] = ( (length - 1) * rep[dimension] + point[dimension] ) / length;