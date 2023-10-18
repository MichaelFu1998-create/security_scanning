def __create_grid(self):
        """!
        @brief Creates CLIQUE grid that consists of CLIQUE blocks for clustering process.

        """
        data_sizes, min_corner, max_corner = self.__get_data_size_derscription()
        dimension = len(self.__data[0])

        cell_sizes = [dimension_length / self.__amount_intervals for dimension_length in data_sizes]

        self.__cells = [clique_block() for _ in range(pow(self.__amount_intervals, dimension))]
        iterator = coordinate_iterator(dimension, self.__amount_intervals)

        point_availability = [True] * len(self.__data)
        self.__cell_map = {}
        for index_cell in range(len(self.__cells)):
            logical_location = iterator.get_coordinate()
            iterator.increment()

            self.__cells[index_cell].logical_location = logical_location[:]

            cur_max_corner, cur_min_corner = self.__get_spatial_location(logical_location, min_corner, max_corner, cell_sizes)
            self.__cells[index_cell].spatial_location = spatial_block(cur_max_corner, cur_min_corner)

            self.__cells[index_cell].capture_points(self.__data, point_availability)

            self.__cell_map[self.__location_to_key(logical_location)] = self.__cells[index_cell]