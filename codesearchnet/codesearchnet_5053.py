def simulate_static(self, steps, time, pattern, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs static simulation of syncpr oscillatory network.
        @details In other words network performs pattern recognition during simulation.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        @param[in] solution (solve_type): Type of solution.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see simulate()
        @see simulate_dynamic()
        
        """
        
        self.__validate_pattern(pattern);
        
        if (self._ccore_network_pointer is not None):
            ccore_instance_dynamic = wrapper.syncpr_simulate_static(self._ccore_network_pointer, steps, time, pattern, solution, collect_dynamic);
            return syncpr_dynamic(None, None, ccore_instance_dynamic);
        
        for i in range(0, len(pattern), 1):
            if (pattern[i] > 0.0):
                self._phases[i] = 0.0;
            else:
                self._phases[i] = math.pi / 2.0;
                
        return super().simulate_static(steps, time, solution, collect_dynamic);