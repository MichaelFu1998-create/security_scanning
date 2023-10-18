def __create_neighbor_searcher(self, data_type):
        """!
        @brief Returns neighbor searcher in line with data type.

        @param[in] data_type (string): Data type (points or distance matrix).

        """
        if data_type == 'points':
            return self.__neighbor_indexes_points
        elif data_type == 'distance_matrix':
            return self.__neighbor_indexes_distance_matrix
        else:
            raise TypeError("Unknown type of data is specified '%s'" % data_type)