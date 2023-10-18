def allocate_correlation_matrix(self, iteration = None):
        """!
        @brief Allocate correlation matrix between oscillators at the specified step of simulation.
               
        @param[in] iteration (uint): Number of iteration of simulation for which correlation matrix should be allocated.
                    If iternation number is not specified, the last step of simulation is used for the matrix allocation.
        
        @return (list) Correlation matrix between oscillators with size [number_oscillators x number_oscillators].
        
        """
        
        if (self._ccore_sync_dynamic_pointer is not None):
            return wrapper.sync_dynamic_allocate_correlation_matrix(self._ccore_sync_dynamic_pointer, iteration);
        
        if ( (self._dynamic is None) or (len(self._dynamic) == 0) ):
            return [];
        
        dynamic = self._dynamic;
        current_dynamic = dynamic[len(dynamic) - 1];
        
        if (iteration is not None):
            current_dynamic = dynamic[iteration];
        
        number_oscillators = len(dynamic[0]);
        affinity_matrix = [ [ 0.0 for i in range(number_oscillators) ] for j in range(number_oscillators) ];
        
        for i in range(number_oscillators):
            for j in range(number_oscillators):
                phase1 = current_dynamic[i];
                phase2 = current_dynamic[j];
                
                affinity_matrix[i][j] = abs(math.sin(phase1 - phase2));
                
        return affinity_matrix;