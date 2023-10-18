def allocate_phase_matrix(self, grid_width = None, grid_height = None, iteration = None):
        """!
        @brief Returns 2D matrix of phase values of oscillators at the specified iteration of simulation.
        @details User should ensure correct matrix sizes in line with following expression grid_width x grid_height that should be equal to 
                  amount of oscillators otherwise exception is thrown. If grid_width or grid_height are not specified than phase matrix size 
                  will by calculated automatically by square root.
        
        @param[in] grid_width (uint): Width of the allocated matrix.
        @param[in] grid_height (uint): Height of the allocated matrix.
        @param[in] iteration (uint): Number of iteration of simulation for which correlation matrix should be allocated.
                    If iternation number is not specified, the last step of simulation is used for the matrix allocation.
        
        @return (list) Phase value matrix of oscillators with size [number_oscillators x number_oscillators].
        
        """
        
        output_dynamic = self.output;
        
        if ( (output_dynamic is None) or (len(output_dynamic) == 0) ):
            return [];
        
        current_dynamic = output_dynamic[len(output_dynamic) - 1];
        if (iteration is not None):
            current_dynamic = output_dynamic[iteration];
        
        width_matrix = grid_width;
        height_matrix = grid_height;
        number_oscillators = len(current_dynamic);
        if ( (width_matrix is None) or (height_matrix is None) ):
            width_matrix = int(math.ceil(math.sqrt(number_oscillators)));
            height_matrix = width_matrix;

        if (number_oscillators != width_matrix * height_matrix):
            raise NameError("Impossible to allocate phase matrix with specified sizes, amout of neurons should be equal to grid_width * grid_height.");
        
        
        phase_matrix = [ [ 0.0 for i in range(width_matrix) ] for j in range(height_matrix) ];
        for i in range(height_matrix):
            for j in range(width_matrix):
                phase_matrix[i][j] = current_dynamic[j + i * width_matrix];
        
        return phase_matrix;