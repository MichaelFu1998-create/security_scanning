def split(self, split_dimension, cache_points):
        """!
        @brief Split BANG-block into two new blocks in specified dimension.

        @param[in] split_dimension (uint): Dimension where block should be split.
        @param[in] cache_points (bool): If True then covered points are cached. Used for leaf blocks.

        @return (tuple) Pair of BANG-block that were formed from the current.

        """
        left_region_number = self.__region_number
        right_region_number = self.__region_number + 2 ** self.__level

        first_spatial_block, second_spatial_block = self.__spatial_block.split(split_dimension)

        left = bang_block(self.__data, left_region_number, self.__level + 1, first_spatial_block, cache_points)
        right = bang_block(self.__data, right_region_number, self.__level + 1, second_spatial_block, cache_points)

        return left, right