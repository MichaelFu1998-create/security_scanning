def allocate_map_coloring(self, tolerance = 0.1):
        """!
        @brief Allocates coloring map for graph that has been processed.
        
        @param[in] tolerance (double): Defines maximum deviation between phases.
        
        @return (list) Colors for each node (index of node in graph), for example [color1, color2, color2, ...].
        
        """
        
        clusters = self.allocate_color_clusters(tolerance);
        number_oscillators = len(self._dynamic[0]);
        
        coloring_map = [0] * number_oscillators;
        
        for color_index in range(len(clusters)):
            for node_index in clusters[color_index]:
                coloring_map[node_index] = color_index;
                
        return coloring_map;