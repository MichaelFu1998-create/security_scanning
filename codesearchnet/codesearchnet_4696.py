def show_output_dynamic(fsync_output_dynamic):
        """!
        @brief Shows output dynamic (output of each oscillator) during simulation.
        
        @param[in] fsync_output_dynamic (fsync_dynamic): Output dynamic of the fSync network.
        
        @see show_output_dynamics
        
        """
        
        pyclustering.utils.draw_dynamics(fsync_output_dynamic.time, fsync_output_dynamic.output, x_title = "t", y_title = "amplitude");