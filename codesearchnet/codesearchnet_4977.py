def get_distance_matrix(self):
        """!
        @brief Calculates distance matrix (U-matrix).
        @details The U-Matrix visualizes based on the distance in input space between a weight vector and its neighbors on map.
        
        @return (list) Distance matrix (U-matrix).
        
        @see show_distance_matrix()
        @see get_density_matrix()
        
        """
        if self.__ccore_som_pointer is not None:
            self._weights = wrapper.som_get_weights(self.__ccore_som_pointer)
            
            if self._conn_type != type_conn.func_neighbor:
                self._neighbors = wrapper.som_get_neighbors(self.__ccore_som_pointer)
            
        distance_matrix = [[0.0] * self._cols for i in range(self._rows)]
        
        for i in range(self._rows):
            for j in range(self._cols):
                neuron_index = i * self._cols + j
                
                if self._conn_type == type_conn.func_neighbor:
                    self._create_connections(type_conn.grid_eight)
                
                for neighbor_index in self._neighbors[neuron_index]:
                    distance_matrix[i][j] += euclidean_distance_square(self._weights[neuron_index], self._weights[neighbor_index])
                    
                distance_matrix[i][j] /= len(self._neighbors[neuron_index])
    
        return distance_matrix