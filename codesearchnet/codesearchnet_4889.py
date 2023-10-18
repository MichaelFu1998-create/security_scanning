def is_neighbor(self, block):
        """!
        @brief Performs calculation to identify whether specified block is neighbor of current block.
        @details It also considers diagonal blocks as neighbors.

        @param[in] block (spatial_block): Another block that is check whether it is neighbor.

        @return (bool) True is blocks are neighbors, False otherwise.

        """
        if block is not self:
            block_max_corner, _ = block.get_corners()
            dimension = len(block_max_corner)
            neighborhood_score = self.__calculate_neighborhood(block_max_corner)

            if neighborhood_score == dimension:
                return True

        return False