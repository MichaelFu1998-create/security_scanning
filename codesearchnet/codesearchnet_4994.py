def show_phase_matrix(sync_output_dynamic, grid_width = None, grid_height = None, iteration = None):
        """!
        @brief Shows 2D matrix of phase values of oscillators at the specified iteration.
        @details User should ensure correct matrix sizes in line with following expression grid_width x grid_height that should be equal to 
                  amount of oscillators otherwise exception is thrown. If grid_width or grid_height are not specified than phase matrix size 
                  will by calculated automatically by square root.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network whose phase matrix should be shown.
        @param[in] grid_width (uint): Width of the phase matrix.
        @param[in] grid_height (uint): Height of the phase matrix.
        @param[in] iteration (uint): Number of iteration of simulation for which correlation matrix should be allocated.
                    If iternation number is not specified, the last step of simulation is used for the matrix allocation.
        
        """
        
        _ = plt.figure();
        phase_matrix = sync_output_dynamic.allocate_phase_matrix(grid_width, grid_height, iteration);
        
        plt.imshow(phase_matrix, cmap = plt.get_cmap('jet'), interpolation='kaiser', vmin = 0.0, vmax = 2.0 * math.pi); 
        plt.show();