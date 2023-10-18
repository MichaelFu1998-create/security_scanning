def allocate_sync_ensembles(self, tolerance = 0.01, indexes = None, iteration = None):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
               
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        @param[in] indexes (list): List of real object indexes and it should be equal to amount of oscillators (in case of 'None' - indexes are in range [0; amount_oscillators]).
        @param[in] iteration (uint): Iteration of simulation that should be used for allocation.
        
        @return (list) Grours (lists) of indexes of synchronous oscillators.
                For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """
        
        if (self._ccore_sync_dynamic_pointer is not None):
            ensembles = wrapper.sync_dynamic_allocate_sync_ensembles(self._ccore_sync_dynamic_pointer, tolerance, iteration);
            
            if (indexes is not None):
                for ensemble in ensembles:
                    for index in range(len(ensemble)):
                        ensemble[index] = indexes[ ensemble[index] ];
                
            return ensembles;
        
        if ( (self._dynamic is None) or (len(self._dynamic) == 0) ):
            return [];
        
        number_oscillators = len(self._dynamic[0]);
        last_state = None;
        
        if (iteration is None):
            last_state = self._dynamic[len(self._dynamic) - 1];
        else:
            last_state = self._dynamic[iteration];
        
        clusters = [];
        if (number_oscillators > 0):
            clusters.append([0]);
        
        for i in range(1, number_oscillators, 1):
            cluster_allocated = False;
            for cluster in clusters:
                for neuron_index in cluster:
                    last_state_shifted = abs(last_state[i] - 2 * pi);
                    
                    if ( ( (last_state[i] < (last_state[neuron_index] + tolerance)) and (last_state[i] > (last_state[neuron_index] - tolerance)) ) or
                         ( (last_state_shifted < (last_state[neuron_index] + tolerance)) and (last_state_shifted > (last_state[neuron_index] - tolerance)) ) ):
                        cluster_allocated = True;
                        
                        real_index = i;
                        if (indexes is not None):
                            real_index = indexes[i];
                        
                        cluster.append(real_index);
                        break;
                
                if (cluster_allocated == True):
                    break;
            
            if (cluster_allocated == False):
                clusters.append([i]);
        
        return clusters;