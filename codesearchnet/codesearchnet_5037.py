def show_dynamic_matrix(cnn_output_dynamic):
        """!
        @brief Shows output dynamic as matrix in grey colors.
        @details This type of visualization is convenient for observing allocated clusters.
        
        @param[in] cnn_output_dynamic (cnn_dynamic): Output dynamic of the chaotic neural network.
        
        @see show_output_dynamic
        @see show_observation_matrix
        
        """
        
        network_dynamic = numpy.array(cnn_output_dynamic.output)
        
        plt.imshow(network_dynamic.T, cmap = plt.get_cmap('gray'), interpolation='None', vmin = 0.0, vmax = 1.0)
        plt.show()