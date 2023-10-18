def __create_dynamic_connections(self):
        """!
        @brief Create dynamic connection in line with input stimulus.
        
        """
        
        if (self._stimulus is None):
            raise NameError("Stimulus should initialed before creation of the dynamic connections in the network.");
        
        self._dynamic_coupling = [ [0] * self._num_osc for i in range(self._num_osc)];
        
        for i in range(self._num_osc):
            neighbors = self.get_neighbors(i);
            
            if ( (len(neighbors) > 0) and (self._stimulus[i] > 0) ):
                number_stimulated_neighbors = 0.0;
                for j in neighbors:
                    if (self._stimulus[j] > 0):
                        number_stimulated_neighbors += 1.0;
                
                if (number_stimulated_neighbors > 0):
                    dynamic_weight = self._params.Wt / number_stimulated_neighbors;
                    
                    for j in neighbors:
                        self._dynamic_coupling[i][j] = dynamic_weight;