def simulate_static(self, steps, time, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs static simulation of oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solution.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see simulate()
        @see simulate_dynamic()
        
        """
        
        if (self._ccore_network_pointer is not None):
            ccore_instance_dynamic = wrapper.sync_simulate_static(self._ccore_network_pointer, steps, time, solution, collect_dynamic);
            return sync_dynamic(None, None, ccore_instance_dynamic);
        
        dyn_phase = [];
        dyn_time = [];
        
        if (collect_dynamic == True):
            dyn_phase.append(self._phases);
            dyn_time.append(0);
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._phases = self._calculate_phases(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_phase.append(self._phases);
                dyn_time.append(t);
        
        if (collect_dynamic != True):
            dyn_phase.append(self._phases);
            dyn_time.append(time);
                        
        output_sync_dynamic = sync_dynamic(dyn_phase, dyn_time);
        return output_sync_dynamic;