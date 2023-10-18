def __get_rectangle_description(block, pair):
        """!
        @brief Create rectangle description for block in specific dimension.

        @param[in] pair (tuple): Pair of coordinate index that should be displayed.
        @param[in] block (bang_block): BANG-block that should be displayed

        @return (tuple) Pair of corners that describes rectangle.

        """
        max_corner, min_corner = block.get_spatial_block().get_corners()

        max_corner = [max_corner[pair[0]], max_corner[pair[1]]]
        min_corner = [min_corner[pair[0]], min_corner[pair[1]]]

        if pair == (0, 0):
            max_corner[1], min_corner[1] = 1.0, -1.0

        return max_corner, min_corner