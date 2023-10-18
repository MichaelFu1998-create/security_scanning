def __get_start_stop_iterations(self, start_iteration, stop_iteration):
        """!
        @brief Aplly rules for start_iteration and stop_iteration parameters.

        @param[in] start_iteration (uint): The first iteration that is used for calculation.
        @param[in] stop_iteration (uint): The last iteration that is used for calculation.
        
        @return (tuple) New the first iteration and the last.
        
        """
        if (start_iteration is None):
            start_iteration = len(self) - 1;
        
        if (stop_iteration is None):
            stop_iteration = start_iteration + 1;
        
        return (start_iteration, stop_iteration);