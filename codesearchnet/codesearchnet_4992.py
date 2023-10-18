def show_output_dynamic(sync_output_dynamic):
        """!
        @brief Shows output dynamic (output of each oscillator) during simulation.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        
        @see show_output_dynamics
        
        """
        
        draw_dynamics(sync_output_dynamic.time, sync_output_dynamic.output, x_title = "t", y_title = "phase", y_lim = [0, 2 * 3.14]);