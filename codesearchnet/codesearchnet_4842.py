def __process_by_ccore(self):
        """!
        @brief Performs cluster analysis using C++ implementation of CLIQUE algorithm that is used by default if
                user's target platform is supported.

        """
        (self.__clusters, self.__noise, block_logical_locations, block_max_corners, block_min_corners, block_points) = \
            wrapper.clique(self.__data, self.__amount_intervals, self.__density_threshold)

        amount_cells = len(block_logical_locations)
        for i in range(amount_cells):
            self.__cells.append(clique_block(block_logical_locations[i],
                                             spatial_block(block_max_corners[i], block_min_corners[i]),
                                             block_points[i],
                                             True))