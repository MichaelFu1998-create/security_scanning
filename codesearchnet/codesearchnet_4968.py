def _create_initial_weights(self, init_type):
        """!
        @brief Creates initial weights for neurons in line with the specified initialization.
        
        @param[in] init_type (type_init): Type of initialization of initial neuron weights (random, random in center of the input data, random distributed in data, ditributed in line with uniform grid).
        
        """
        
        dim_info = dimension_info(self._data)
        
        step_x = dim_info.get_center()[0]
        if self._rows > 1: step_x = dim_info.get_width()[0] / (self._rows - 1);
        
        step_y = 0.0
        if dim_info.get_dimensions() > 1:
            step_y = dim_info.get_center()[1]
            if self._cols > 1: step_y = dim_info.get_width()[1] / (self._cols - 1);
                      
        # generate weights (topological coordinates)
        random.seed()
        
        # Uniform grid.
        if init_type == type_init.uniform_grid:
            # Predefined weights in line with input data.
            self._weights = [ [ [] for i in range(dim_info.get_dimensions()) ] for j in range(self._size)]
            for i in range(self._size):
                location = self._location[i]
                for dim in range(dim_info.get_dimensions()):
                    if dim == 0:
                        if self._rows > 1:
                            self._weights[i][dim] = dim_info.get_minimum_coordinate()[dim] + step_x * location[dim]
                        else:
                            self._weights[i][dim] = dim_info.get_center()[dim]
                            
                    elif dim == 1:
                        if self._cols > 1:
                            self._weights[i][dim] = dim_info.get_minimum_coordinate()[dim] + step_y * location[dim]
                        else:
                            self._weights[i][dim] = dim_info.get_center()[dim]
                    else:
                        self._weights[i][dim] = dim_info.get_center()[dim]
        
        elif init_type == type_init.random_surface:
            # Random weights at the full surface.
            self._weights = [[random.uniform(dim_info.get_minimum_coordinate()[i], dim_info.get_maximum_coordinate()[i]) for i in range(dim_info.get_dimensions())] for _ in range(self._size)]
        
        elif init_type == type_init.random_centroid:
            # Random weights at the center of input data.
            self._weights = [[(random.random() + dim_info.get_center()[i])  for i in range(dim_info.get_dimensions())] for _ in range(self._size)]
        
        else:
            # Random weights of input data.
            self._weights = [[random.random() for i in range(dim_info.get_dimensions())] for _ in range(self._size)]