def __get_start_stop_iterations(sync_output_dynamic, start_iteration, stop_iteration):
        """!
        @brief Apply rule of preparation for start iteration and stop iteration values.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] start_iteration (uint): The first iteration that is used for calculation.
        @param[in] stop_iteration (uint): The last iteration that is used for calculation.
        
        @return (tuple) New values of start and stop iterations.
        
        """
        if (start_iteration is None):
            start_iteration = 0;
        
        if (stop_iteration is None):
            stop_iteration = len(sync_output_dynamic);
        
        return (start_iteration, stop_iteration);