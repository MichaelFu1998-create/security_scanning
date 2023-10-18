def _create_connections(self, radius):
        """!
        @brief Create connections between oscillators in line with input radius of connectivity.
        
        @param[in] radius (double): Connectivity radius between oscillators.
        
        """
        
        if (self._ena_conn_weight is True):
            self._conn_weight = [[0] * self._num_osc for _ in range(0, self._num_osc, 1)];
        
        maximum_distance = 0;
        minimum_distance = float('inf');
        
        # Create connections
        for i in range(0, self._num_osc, 1):
            for j in range(i + 1, self._num_osc, 1):
                    dist = euclidean_distance(self._osc_loc[i], self._osc_loc[j]);
                    
                    if (self._ena_conn_weight is True):
                        self._conn_weight[i][j] = dist;
                        self._conn_weight[j][i] = dist;
                        
                        if (dist > maximum_distance): maximum_distance = dist;
                        if (dist < minimum_distance): minimum_distance = dist;
                    
                    if (dist <= radius):
                        self.set_connection(i, j);
        
        if (self._ena_conn_weight is True):
            multiplier = 1; 
            subtractor = 0;
            
            if (maximum_distance != minimum_distance):
                multiplier = (maximum_distance - minimum_distance);
                subtractor = minimum_distance;
            
            for i in range(0, self._num_osc, 1):
                for j in range(i + 1, self._num_osc, 1):
                    value_conn_weight = (self._conn_weight[i][j] - subtractor) / multiplier;
                    
                    self._conn_weight[i][j] = value_conn_weight;
                    self._conn_weight[j][i] = value_conn_weight;