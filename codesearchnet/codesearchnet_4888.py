def split(self, dimension):
        """!
        @brief Split current block into two spatial blocks in specified dimension.

        @param[in] dimension (uint): Dimension where current block should be split.

        @return (tuple) Pair of new split blocks from current block.

        """
        first_max_corner = self.__max_corner[:]
        second_min_corner = self.__min_corner[:]

        split_border = (self.__max_corner[dimension] + self.__min_corner[dimension]) / 2.0

        first_max_corner[dimension] = split_border
        second_min_corner[dimension] = split_border

        return spatial_block(first_max_corner, self.__min_corner), spatial_block(self.__max_corner, second_min_corner)