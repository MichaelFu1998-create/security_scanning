def _calculate_states(self, solution, t, step, int_step):
        """!
        @brief Caclculates new state of each oscillator in the network. Returns only excitatory state of oscillators.
        
        @param[in] solution (solve_type): Type solver of the differential equations.
        @param[in] t (double): Current time of simulation.
        @param[in] step (uint): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Differentiation step that is used for solving differential equation.
        
        @return (list) New states of membrance potentials for peripheral oscillators and for cental elements as a list where
                the last two values correspond to central element 1 and 2.
                 
        """
        
        next_membrane           = [0.0] * self._num_osc;
        next_active_sodium      = [0.0] * self._num_osc;
        next_inactive_sodium    = [0.0] * self._num_osc;
        next_active_potassium   = [0.0] * self._num_osc;
        
        # Update states of oscillators
        for index in range (0, self._num_osc, 1):
            result = odeint(self.hnn_state, 
                            [ self._membrane_potential[index], self._active_cond_sodium[index], self._inactive_cond_sodium[index], self._active_cond_potassium[index] ], 
                            numpy.arange(t - step, t, int_step), 
                            (index , ));
                            
            [ next_membrane[index], next_active_sodium[index], next_inactive_sodium[index], next_active_potassium[index] ] = result[len(result) - 1][0:4];        
        
        next_cn_membrane            = [0.0, 0.0];
        next_cn_active_sodium       = [0.0, 0.0];
        next_cn_inactive_sodium     = [0.0, 0.0];
        next_cn_active_potassium    = [0.0, 0.0];
        
        # Update states of central elements
        for index in range(0, len(self._central_element)):
            result = odeint(self.hnn_state, 
                            [ self._central_element[index].membrane_potential, self._central_element[index].active_cond_sodium, self._central_element[index].inactive_cond_sodium, self._central_element[index].active_cond_potassium ], 
                            numpy.arange(t - step, t, int_step), 
                            (self._num_osc + index , ));
                            
            [ next_cn_membrane[index], next_cn_active_sodium[index], next_cn_inactive_sodium[index], next_cn_active_potassium[index] ] = result[len(result) - 1][0:4];
        
        # Noise generation
        self._noise = [ 1.0 + 0.01 * (random.random() * 2.0 - 1.0) for i in range(self._num_osc)];
        
        # Updating states of PNs
        self.__update_peripheral_neurons(t, step, next_membrane, next_active_sodium, next_inactive_sodium, next_active_potassium);
        
        # Updation states of CN
        self.__update_central_neurons(t, next_cn_membrane, next_cn_active_sodium, next_cn_inactive_sodium, next_cn_active_potassium);
        
        return (next_membrane, next_cn_membrane);