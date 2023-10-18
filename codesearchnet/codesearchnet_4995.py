def show_order_parameter(sync_output_dynamic, start_iteration = None, stop_iteration = None):
        """!
        @brief Shows evolution of order parameter (level of global synchronization in the network).
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network whose evolution of global synchronization should be visualized.
        @param[in] start_iteration (uint): The first iteration that is used for calculation, if 'None' then the first is used
        @param[in] stop_iteration (uint): The last iteration that is used for calculation, if 'None' then the last is used.
        
        """
        
        (start_iteration, stop_iteration) = sync_visualizer.__get_start_stop_iterations(sync_output_dynamic, start_iteration, stop_iteration);
        
        order_parameter = sync_output_dynamic.calculate_order_parameter(start_iteration, stop_iteration);
        axis = plt.subplot(111);
        plt.plot(sync_output_dynamic.time[start_iteration:stop_iteration], order_parameter, 'b-', linewidth = 2.0);
        set_ax_param(axis, "t", "R (order parameter)", None, [0.0, 1.05]);
        
        plt.show();