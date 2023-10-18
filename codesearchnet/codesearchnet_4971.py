def _adaptation(self, index, x):
        """!
        @brief Change weight of neurons in line with won neuron.
        
        @param[in] index (uint): Index of neuron-winner.
        @param[in] x (list): Input pattern from the input data set.
        
        """
        
        dimension = len(self._weights[0])
        
        if self._conn_type == type_conn.func_neighbor:
            for neuron_index in range(self._size):
                distance = self._sqrt_distances[index][neuron_index]
                
                if distance < self._local_radius:
                    influence = math.exp(-(distance / (2.0 * self._local_radius)))
                    
                    for i in range(dimension):
                        self._weights[neuron_index][i] = self._weights[neuron_index][i] + self._learn_rate * influence * (x[i] - self._weights[neuron_index][i])
                    
        else:
            for i in range(dimension):
                self._weights[index][i] = self._weights[index][i] + self._learn_rate * (x[i] - self._weights[index][i])
                
            for neighbor_index in self._neighbors[index]: 
                distance = self._sqrt_distances[index][neighbor_index]
                if distance < self._local_radius:
                    influence = math.exp(-(distance / (2.0 * self._local_radius)))
                    
                    for i in range(dimension):       
                        self._weights[neighbor_index][i] = self._weights[neighbor_index][i] + self._learn_rate * influence * (x[i] - self._weights[neighbor_index][i])