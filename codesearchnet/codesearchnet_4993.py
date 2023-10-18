def show_correlation_matrix(sync_output_dynamic, iteration = None):
        """!
        @brief Shows correlation matrix between oscillators at the specified iteration.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] iteration (uint): Number of interation of simulation for which correlation matrix should be allocated.
                                      If iternation number is not specified, the last step of simulation is used for the matrix allocation.
        
        """
        
        _ = plt.figure();
        correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(iteration);
        
        plt.imshow(correlation_matrix, cmap = plt.get_cmap('cool'), interpolation='kaiser', vmin = 0.0, vmax = 1.0); 
        plt.show();