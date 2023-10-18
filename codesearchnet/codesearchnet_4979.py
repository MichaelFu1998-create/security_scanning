def get_density_matrix(self, surface_divider = 20.0):
        """!
        @brief Calculates density matrix (P-Matrix).
        
        @param[in] surface_divider (double): Divider in each dimension that affect radius for density measurement.
        
        @return (list) Density matrix (P-Matrix).
        
        @see get_distance_matrix()
        
        """
        
        if self.__ccore_som_pointer is not None:
            self._weights = wrapper.som_get_weights(self.__ccore_som_pointer)
        
        density_matrix = [[0] * self._cols for i in range(self._rows)]
        dimension = len(self._weights[0])
        
        dim_max = [ float('-Inf') ] * dimension
        dim_min = [ float('Inf') ] * dimension
        
        for weight in self._weights:
            for index_dim in range(dimension):
                if weight[index_dim] > dim_max[index_dim]:
                    dim_max[index_dim] = weight[index_dim]
                
                if weight[index_dim] < dim_min[index_dim]:
                    dim_min[index_dim] = weight[index_dim]
        
        radius = [0.0] * len(self._weights[0])
        for index_dim in range(dimension):
            radius[index_dim] = ( dim_max[index_dim] - dim_min[index_dim] ) / surface_divider

        ## TODO: do not use data
        for point in self._data:
            for index_neuron in range(len(self)):
                point_covered = True
                
                for index_dim in range(dimension):
                    if abs(point[index_dim] - self._weights[index_neuron][index_dim]) > radius[index_dim]:
                        point_covered = False
                        break
                
                row = int(math.floor(index_neuron / self._cols))
                col = index_neuron - row * self._cols
                
                if point_covered is True:
                    density_matrix[row][col] += 1
        
        return density_matrix