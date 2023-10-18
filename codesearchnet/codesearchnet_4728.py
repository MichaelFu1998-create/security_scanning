def __neighbor_indexes_points(self, index_point):
        """!
        @brief Return neighbors of the specified object in case of sequence of points.

        @param[in] index_point (uint): Index point whose neighbors are should be found.

        @return (list) List of indexes of neighbors in line the connectivity radius.

        """
        kdnodes = self.__kdtree.find_nearest_dist_nodes(self.__pointer_data[index_point], self.__eps)
        return [node_tuple[1].payload for node_tuple in kdnodes if node_tuple[1].payload != index_point]