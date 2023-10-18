def __get_spatial_location(self, logical_location, min_corner, max_corner, cell_sizes):
        """!
        @brief Calculates spatial location for CLIQUE block with logical coordinates defined by logical_location.

        @param[in] logical_location (list): Logical location of CLIQUE block for that spatial location should be calculated.
        @param[in] min_corner (list): Minimum corner of an input data.
        @param[in] max_corner (list): Maximum corner of an input data.
        @param[in] cell_sizes (list): Size of CLIQUE block in each dimension.

        @return (list, list): Maximum and minimum corners for the specified CLIQUE block.

        """
        cur_min_corner = min_corner[:]
        cur_max_corner = min_corner[:]
        dimension = len(self.__data[0])
        for index_dimension in range(dimension):
            cur_min_corner[index_dimension] += cell_sizes[index_dimension] * logical_location[index_dimension]

            if logical_location[index_dimension] == self.__amount_intervals - 1:
                cur_max_corner[index_dimension] = max_corner[index_dimension]
            else:
                cur_max_corner[index_dimension] = cur_min_corner[index_dimension] + cell_sizes[index_dimension]

        return cur_max_corner, cur_min_corner