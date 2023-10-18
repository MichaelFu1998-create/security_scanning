def __calculate_radius(self, number_neighbors, radius):
        """!
        @brief Calculate new connectivity radius.
        
        @param[in] number_neighbors (uint): Average amount of neighbors that should be connected by new radius.
        @param[in] radius (double): Current connectivity radius.
        
        @return New connectivity radius.
        
        """
        
        if (number_neighbors >= len(self._osc_loc)):
            return radius * self.__increase_persent + radius;
        
        return average_neighbor_distance(self._osc_loc, number_neighbors);