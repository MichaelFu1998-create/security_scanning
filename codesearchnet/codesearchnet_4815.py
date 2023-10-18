def simulate(self, steps, time, stimulus, solution = solve_type.RK4, collect_dynamic = True):
        """!
        @brief Performs static simulation of LEGION oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] stimulus (list): Stimulus for oscillators, number of stimulus should be equal to number of oscillators,
                   example of stimulus for 5 oscillators [0, 0, 1, 1, 0], value of stimulus is defined by parameter 'I'.
        @param[in] solution (solve_type): Method that is used for differential equation.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        """
        
        if (self.__ccore_legion_pointer is not None):
            pointer_dynamic = wrapper.legion_simulate(self.__ccore_legion_pointer, steps, time, solution, collect_dynamic, stimulus);
            return legion_dynamic(None, None, None, pointer_dynamic);
        
        # Check solver before simulation
        if (solution == solve_type.FAST):
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.");
        
        elif (solution == solve_type.RKF45):
            raise NameError("Solver RKF45 is not support in python version. RKF45 is supported in CCORE implementation.");
        
        # set stimulus
        self.__create_stimulus(stimulus);
            
        # calculate dynamic weights
        self.__create_dynamic_connections();
        
        dyn_exc = None;
        dyn_time = None;
        dyn_ginh = None;
        
        # Store only excitatory of the oscillator
        if (collect_dynamic == True):
            dyn_exc = [];
            dyn_time = [];
            dyn_ginh = [];
            
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_exc.append(self._excitatory);
                dyn_time.append(t);
                dyn_ginh.append(self._global_inhibitor);
            else:
                dyn_exc = self._excitatory;
                dyn_time = t;
                dyn_ginh = self._global_inhibitor;
        
        return legion_dynamic(dyn_exc, dyn_ginh, dyn_time);