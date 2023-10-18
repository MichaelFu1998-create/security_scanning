def find_nearest_dist_nodes(self, point, distance):
        """!
        @brief Find neighbors that are located in area that is covered by specified distance.
        
        @param[in] point (list): Coordinates that is considered as centroind for searching.
        @param[in] distance (double): Distance from the center where seaching is performed.
        
        @return (list) Neighbors in area that is specified by point (center) and distance (radius).
        
        """

        best_nodes = []
        if self.__root is not None:
            self.__recursive_nearest_nodes(point, distance, distance * distance, self.__root, best_nodes)

        return best_nodes