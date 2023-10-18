def find_nearest_dist_node(self, point, distance, retdistance = False):
        """!
        @brief Find nearest neighbor in area with radius = distance.
        
        @param[in] point (list): Maximum distance where neighbors are searched.
        @param[in] distance (double): Maximum distance where neighbors are searched.
        @param[in] retdistance (bool): If True - returns neighbors with distances to them, otherwise only neighbors is returned.
        
        @return (node|list) Nearest neighbor if 'retdistance' is False and list with two elements [node, distance] if 'retdistance' is True,
                 where the first element is pointer to node and the second element is distance to it.
        
        """
        
        best_nodes = self.find_nearest_dist_nodes(point, distance)
            
        if best_nodes == []:
            return None
        
        nearest = min(best_nodes, key = lambda item: item[0])
        
        if retdistance is True:
            return nearest
        else:
            return nearest[1]