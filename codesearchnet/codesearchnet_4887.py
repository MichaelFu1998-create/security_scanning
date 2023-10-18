def __split_block(self, block, split_dimension, cache_require, current_level_blocks):
        """!
        @brief Split specific block in specified dimension.
        @details Split is not performed for block whose density is lower than threshold value, such blocks are putted to
                  leafs.

        @param[in] block (bang_block): BANG-block that should be split.
        @param[in] split_dimension (uint): Dimension at which splitting should be performed.
        @param[in] cache_require (bool): Defines when points in cache should be stored during density calculation.
        @param[in|out] current_level_blocks (list): Block storage at the current level where new blocks should be added.

        """
        if block.get_density() <= self.__density_threshold or len(block) <= self.__amount_density:
            self.__leafs.append(block)

        else:
            left, right = block.split(split_dimension, cache_require)
            current_level_blocks.append(left)
            current_level_blocks.append(right)