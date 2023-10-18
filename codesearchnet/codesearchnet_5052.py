def simulate_dynamic(self, pattern, order = 0.998, solution = solve_type.RK4, collect_dynamic = False, step = 0.1, int_step = 0.01, threshold_changes = 0.0000001):
        """!
        @brief Performs dynamic simulation of the network until stop condition is not reached.
        @details In other words network performs pattern recognition during simulation. 
                 Stop condition is defined by input argument 'order' that represents memory order, but
                 process of simulation can be stopped if convergance rate is low whose threshold is defined
                 by the argument 'threshold_changes'.
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        @param[in] order (double): Order of process synchronization, distributed 0..1.
        @param[in] solution (solve_type): Type of solution.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        @param[in] step (double): Time step of one iteration of simulation.
        @param[in] int_step (double): Integration step, should be less than step.
        @param[in] threshold_changes (double): Additional stop condition that helps prevent infinite simulation, defines limit of changes of oscillators between current and previous steps.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see simulate()
        @see simulate_static()
        
        """
        
        self.__validate_pattern(pattern);
        
        if (self._ccore_network_pointer is not None):
            ccore_instance_dynamic = wrapper.syncpr_simulate_dynamic(self._ccore_network_pointer, pattern, order, solution, collect_dynamic, step);
            return syncpr_dynamic(None, None, ccore_instance_dynamic);
        
        for i in range(0, len(pattern), 1):
            if (pattern[i] > 0.0):
                self._phases[i] = 0.0;
            else:
                self._phases[i] = math.pi / 2.0;
        
        # For statistics and integration
        time_counter = 0;
        
        # Prevent infinite loop. It's possible when required state cannot be reached.
        previous_order = 0;
        current_order = self.__calculate_memory_order(pattern);
        
        # If requested input dynamics
        dyn_phase = [];
        dyn_time = [];
        if (collect_dynamic == True):
            dyn_phase.append(self._phases);
            dyn_time.append(0);
        
        # Execute until sync state will be reached
        while (current_order < order):
            # update states of oscillators
            self._phases = self._calculate_phases(solution, time_counter, step, int_step);
            
            # update time
            time_counter += step;
            
            # if requested input dynamic
            if (collect_dynamic == True):
                dyn_phase.append(self._phases);
                dyn_time.append(time_counter);
                
            # update orders
            previous_order = current_order;
            current_order = self.__calculate_memory_order(pattern);
            
            # hang prevention
            if (abs(current_order - previous_order) < threshold_changes):
                break;
        
        if (collect_dynamic != True):
            dyn_phase.append(self._phases);
            dyn_time.append(time_counter);
        
        output_sync_dynamic = syncpr_dynamic(dyn_phase, dyn_time, None);
        return output_sync_dynamic;