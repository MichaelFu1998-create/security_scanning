def __update_cluster_dendrogram(self, index_cluster, blocks):
        """!
        @brief Append clustered blocks to dendrogram.

        @param[in] index_cluster (uint): Cluster index that was assigned to blocks.
        @param[in] blocks (list): Blocks that were clustered.

        """
        if len(self.__dendrogram) <= index_cluster:
            self.__dendrogram.append([])

        blocks = sorted(blocks, key=lambda block: block.get_density(), reverse=True)
        self.__dendrogram[index_cluster] += blocks