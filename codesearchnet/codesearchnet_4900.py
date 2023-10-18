def __expand_cluster_block(self, block, cluster_index, leaf_blocks, unhandled_block_indexes):
        """!
        @brief Expand cluster from specific block that is considered as a central block.

        @param[in] block (bang_block): Block that is considered as a central block for cluster.
        @param[in] cluster_index (uint): Index of cluster that is assigned to blocks that forms new cluster.
        @param[in] leaf_blocks (list): Leaf BANG-blocks that are considered during cluster formation.
        @param[in] unhandled_block_indexes (set): Set of candidates (BANG block indexes) to become a cluster member. The
                    parameter helps to reduce traversing among BANG-block providing only restricted set of block that
                    should be considered.

        """

        block.set_cluster(cluster_index)
        self.__update_cluster_dendrogram(cluster_index, [block])

        neighbors = self.__find_block_neighbors(block, leaf_blocks, unhandled_block_indexes)
        self.__update_cluster_dendrogram(cluster_index, neighbors)

        for neighbor in neighbors:
            neighbor.set_cluster(cluster_index)
            neighbor_neighbors = self.__find_block_neighbors(neighbor, leaf_blocks, unhandled_block_indexes)
            self.__update_cluster_dendrogram(cluster_index, neighbor_neighbors)

            neighbors += neighbor_neighbors