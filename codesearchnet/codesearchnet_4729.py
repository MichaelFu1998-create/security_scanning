def __neighbor_indexes_distance_matrix(self, index_point):
        """!
        @brief Return neighbors of the specified object in case of distance matrix.

        @param[in] index_point (uint): Index point whose neighbors are should be found.

        @return (list) List of indexes of neighbors in line the connectivity radius.

        """
        distances = self.__pointer_data[index_point]
        return [index_neighbor for index_neighbor in range(len(distances))
                if ((distances[index_neighbor] <= self.__eps) and (index_neighbor != index_point))]