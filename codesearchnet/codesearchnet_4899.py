def __allocate_clusters(self):
        """!
        @brief Performs cluster allocation using leafs of tree in BANG directory (the smallest cells).

        """
        leaf_blocks = self.__directory.get_leafs()
        unhandled_block_indexes = set([i for i in range(len(leaf_blocks)) if leaf_blocks[i].get_density() > self.__density_threshold])

        current_block = self.__find_block_center(leaf_blocks, unhandled_block_indexes)
        cluster_index = 0

        while current_block is not None:
            if current_block.get_density() <= self.__density_threshold or len(current_block) <= self.__amount_threshold:
                break

            self.__expand_cluster_block(current_block, cluster_index, leaf_blocks, unhandled_block_indexes)

            current_block = self.__find_block_center(leaf_blocks, unhandled_block_indexes)
            cluster_index += 1

        self.__store_clustering_results(cluster_index, leaf_blocks)