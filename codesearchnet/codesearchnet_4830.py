def simulate_static(self, steps, time, solution = solve_type.RK4):
        """!
        @brief Performs static simulation of oscillatory network based on Hodgkin-Huxley neuron model.
        @details Output dynamic is sensible to amount of steps of simulation and solver of differential equation.
                  Python implementation uses 'odeint' from 'scipy', CCORE uses classical RK4 and RFK45 methods,
                  therefore in case of CCORE HHN (Hodgkin-Huxley network) amount of steps should be greater than in
                  case of Python HHN.

        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solver for differential equations.
        
        @return (tuple) Dynamic of oscillatory network represented by (time, peripheral neurons dynamic, central elements
                dynamic), where types are (list, list, list).
        
        """
        
        # Check solver before simulation
        if (solution == solve_type.FAST):
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.");
        
        self._membrane_dynamic_pointer = None;
        
        if (self.__ccore_hhn_pointer is not None):
            self.__ccore_hhn_dynamic_pointer = wrapper.hhn_dynamic_create(True, False, False, False);
            wrapper.hhn_simulate(self.__ccore_hhn_pointer, steps, time, solution, self._stimulus, self.__ccore_hhn_dynamic_pointer);
            
            peripheral_membrane_potential = wrapper.hhn_dynamic_get_peripheral_evolution(self.__ccore_hhn_dynamic_pointer, 0);
            central_membrane_potential = wrapper.hhn_dynamic_get_central_evolution(self.__ccore_hhn_dynamic_pointer, 0);
            dynamic_time = wrapper.hhn_dynamic_get_time(self.__ccore_hhn_dynamic_pointer);
            
            self._membrane_dynamic_pointer = peripheral_membrane_potential;

            wrapper.hhn_dynamic_destroy(self.__ccore_hhn_dynamic_pointer);
            
            return (dynamic_time, peripheral_membrane_potential, central_membrane_potential);
        
        if (solution == solve_type.RKF45):
            raise NameError("Solver RKF45 is not support in python version.");
        
        dyn_peripheral = [ self._membrane_potential[:] ];
        dyn_central = [ [0.0, 0.0] ];
        dyn_time = [ 0.0 ];
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            (memb_peripheral, memb_central) = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            dyn_peripheral.append(memb_peripheral);
            dyn_central.append(memb_central);
            dyn_time.append(t);
        
        self._membrane_dynamic_pointer = dyn_peripheral;
        return (dyn_time, dyn_peripheral, dyn_central);