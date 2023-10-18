def __find_block_neighbors(self, block, level_blocks, unhandled_block_indexes):
        """!
        @brief Search block neighbors that are parts of new clusters (density is greater than threshold and that are
                not cluster members yet), other neighbors are ignored.

        @param[in] block (bang_block): BANG-block for which neighbors should be found (which can be part of cluster).
        @param[in] level_blocks (list): BANG-blocks on specific level.
        @param[in] unhandled_block_indexes (set): Blocks that have not been processed yet.

        @return (list) Block neighbors that can become part of cluster.

        """
        neighbors = []

        handled_block_indexes = []
        for unhandled_index in unhandled_block_indexes:
            if block.is_neighbor(level_blocks[unhandled_index]):
                handled_block_indexes.append(unhandled_index)
                neighbors.append(level_blocks[unhandled_index])

                # Maximum number of neighbors is eight
                if len(neighbors) == 8:
                    break

        for handled_index in handled_block_indexes:
            unhandled_block_indexes.remove(handled_index)

        return neighbors