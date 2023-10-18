def allocate_sync_ensembles(self, steps):
        """!
        @brief Allocate clusters in line with ensembles of synchronous neurons where each synchronous ensemble corresponds to only one cluster.
               
        @param[in] steps (double): Amount of steps from the end that is used for analysis. During specified period chaotic neural network should have stable output
                    otherwise inccorect results are allocated.
        
        @return (list) Grours (lists) of indexes of synchronous oscillators.
                For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """
        
        iterations = steps
        if iterations >= len(self.output):
            iterations = len(self.output)
        
        ensembles = []

        start_iteration = len(self.output) - iterations
        end_iteration = len(self.output)
        
        pattern_matrix = self.__allocate_neuron_patterns(start_iteration, end_iteration)
        
        ensembles.append( [0] )
        
        for index_neuron in range(1, len(self.output[0])):
            neuron_pattern = pattern_matrix[index_neuron][:]
            
            neuron_assigned = False
            
            for ensemble in ensembles:
                ensemble_pattern = pattern_matrix[ensemble[0]][:]

                if neuron_pattern == ensemble_pattern:
                    ensemble.append(index_neuron)
                    neuron_assigned = True
                    break
            
            if neuron_assigned is False:
                ensembles.append( [index_neuron] )
        
        return ensembles