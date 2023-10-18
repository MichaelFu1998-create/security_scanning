def simulate_static(self, steps, time, solution = solve_type.RK4, collect_dynamic = False):
        """!
        @brief Performs static simulation of hysteresis oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solution (solving).
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (hysteresis_dynamic) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        """

        # Check solver before simulation
        if (solution == solve_type.FAST):
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.");
        elif (solution == solve_type.RKF45):
            raise NameError("Solver RKF45 is not support in python version.");

        dyn_state = None;
        dyn_time = None;
        
        if (collect_dynamic == True):
            dyn_state = [];
            dyn_time = [];
            
            dyn_state.append(self._states);
            dyn_time.append(0);
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._states = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic is True):
                dyn_state.append(self._states);
                dyn_time.append(t);
        
        if (collect_dynamic is False):
            dyn_state.append(self._states);
            dyn_time.append(time);
        
        return hysteresis_dynamic(dyn_state, dyn_time);