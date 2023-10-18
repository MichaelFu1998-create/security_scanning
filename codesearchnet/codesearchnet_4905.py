def allocate_map_coloring(self, tolerance, threshold_steps = 10):
        """!
        @brief Returns list of color indexes that are assigned to each object from input data space accordingly.
        
        @param[in] tolerance (double): Tolerance level that define maximal difference between outputs of oscillators in one synchronous ensemble.
        @param[in] threshold_steps (uint): Number of steps from the end of simulation that should be analysed for ensemble allocation.
                    If amount of simulation steps has been less than threshold steps than amount of steps will be reduced to amount
                    of simulation steps.
        
        @remark Results can be obtained only after network simulation (graph processing by the network).
        
        @return (list) Color indexes that are assigned to each object from input data space accordingly.
        
        @see allocate_clusters()
        
        """
        clusters = self.allocate_clusters(tolerance, threshold_steps)
        
        coloring_map = [0] * len(self._dynamic[0])
        
        for color_index in range(len(clusters)):
            for node_index in clusters[color_index]:
                coloring_map[node_index] = color_index
                
        return coloring_map