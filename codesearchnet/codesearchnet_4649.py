def __neighbor_indexes_points(self, optic_object):
        """!
        @brief Return neighbors of the specified object in case of sequence of points.

        @param[in] optic_object (optics_descriptor): Object for which neighbors should be returned in line with connectivity radius.

        @return (list) List of indexes of neighbors in line the connectivity radius.

        """
        kdnodes = self.__kdtree.find_nearest_dist_nodes(self.__sample_pointer[optic_object.index_object], self.__eps)
        return [[node_tuple[1].payload, math.sqrt(node_tuple[0])] for node_tuple in kdnodes if
                node_tuple[1].payload != optic_object.index_object]