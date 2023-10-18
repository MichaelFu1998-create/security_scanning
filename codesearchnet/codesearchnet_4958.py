def show_output_dynamic(pcnn_output_dynamic, separate_representation = False):
        """!
        @brief Shows output dynamic (output of each oscillator) during simulation.
        
        @param[in] pcnn_output_dynamic (pcnn_dynamic): Output dynamic of the pulse-coupled neural network.
        @param[in] separate_representation (list): Consists of lists of oscillators where each such list consists of oscillator indexes that will be shown on separated stage.
        
        """
        
        draw_dynamics(pcnn_output_dynamic.time, pcnn_output_dynamic.output, x_title = "t", y_title = "y(t)", separate = separate_representation)