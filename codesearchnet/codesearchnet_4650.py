def __neighbor_indexes_distance_matrix(self, optic_object):
        """!
        @brief Return neighbors of the specified object in case of distance matrix.

        @param[in] optic_object (optics_descriptor): Object for which neighbors should be returned in line with connectivity radius.

        @return (list) List of indexes of neighbors in line the connectivity radius.

        """
        distances = self.__sample_pointer[optic_object.index_object]
        return [[index_neighbor, distances[index_neighbor]] for index_neighbor in range(len(distances))
                if ((distances[index_neighbor] <= self.__eps) and (index_neighbor != optic_object.index_object))]