def show_observation_matrix(cnn_output_dynamic):
        """!
        @brief Shows observation matrix as black/white blocks.
        @details This type of visualization is convenient for observing allocated clusters.
        
        @param[in] cnn_output_dynamic (cnn_dynamic): Output dynamic of the chaotic neural network.
        
        @see show_output_dynamic
        @see show_dynamic_matrix
        
        """
        
        observation_matrix = numpy.array(cnn_output_dynamic.allocate_observation_matrix())
        plt.imshow(observation_matrix.T, cmap = plt.get_cmap('gray'), interpolation='None', vmin = 0.0, vmax = 1.0)
        plt.show()