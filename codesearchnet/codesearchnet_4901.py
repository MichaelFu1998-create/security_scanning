def __store_clustering_results(self, amount_clusters, leaf_blocks):
        """!
        @brief Stores clustering results in a convenient way.

        @param[in] amount_clusters (uint): Amount of cluster that was allocated during processing.
        @param[in] leaf_blocks (list): Leaf BANG-blocks (the smallest cells).

        """
        self.__clusters = [[] for _ in range(amount_clusters)]
        for block in leaf_blocks:
            index = block.get_cluster()

            if index is not None:
                self.__clusters[index] += block.get_points()
            else:
                self.__noise += block.get_points()

        self.__clusters = [ list(set(cluster)) for cluster in self.__clusters ]
        self.__noise = list(set(self.__noise))