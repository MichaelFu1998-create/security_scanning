def __recursive_nearest_nodes(self, point, distance, sqrt_distance, node_head, best_nodes):
        """!
        @brief Returns list of neighbors such as tuple (distance, node) that is located in area that is covered by distance.
        
        @param[in] point (list): Coordinates that is considered as centroind for searching
        @param[in] distance (double): Distance from the center where seaching is performed.
        @param[in] sqrt_distance (double): Square distance from the center where searching is performed.
        @param[in] node_head (node): Node from that searching is performed.
        @param[in|out] best_nodes (list): List of founded nodes.
        
        """

        if node_head.right is not None:
            minimum = node_head.data[node_head.disc] - distance
            if point[node_head.disc] >= minimum:
                self.__recursive_nearest_nodes(point, distance, sqrt_distance, node_head.right, best_nodes)
        
        if node_head.left is not None:
            maximum = node_head.data[node_head.disc] + distance
            if point[node_head.disc] < maximum:
                self.__recursive_nearest_nodes(point, distance, sqrt_distance, node_head.left, best_nodes)
        
        candidate_distance = euclidean_distance_square(point, node_head.data)
        if candidate_distance <= sqrt_distance:
            best_nodes.append( (candidate_distance, node_head) )