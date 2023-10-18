def __get_data_size_derscription(self):
        """!
        @brief Calculates input data description that is required to create CLIQUE grid.

        @return (list, list, list): Data size in each dimension, minimum and maximum corners.

        """
        min_corner = self.__data[0][:]
        max_corner = self.__data[0][:]

        dimension = len(self.__data[0])

        for index_point in range(1, len(self.__data)):
            for index_dimension in range(dimension):
                coordinate = self.__data[index_point][index_dimension]
                if coordinate > max_corner[index_dimension]:
                    max_corner[index_dimension] = coordinate

                if coordinate < min_corner[index_dimension]:
                    min_corner[index_dimension] = coordinate

        data_sizes = [0.0] * dimension
        for index_dimension in range(dimension):
            data_sizes[index_dimension] = max_corner[index_dimension] - min_corner[index_dimension]

        return data_sizes, min_corner, max_corner