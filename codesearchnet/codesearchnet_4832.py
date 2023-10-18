def __update_peripheral_neurons(self, t, step, next_membrane, next_active_sodium, next_inactive_sodium, next_active_potassium):
        """!
        @brief Update peripheral neurons in line with new values of current in channels.
        
        @param[in] t (doubles): Current time of simulation.
        @param[in] step (uint): Step (time duration) during simulation when states of oscillators should be calculated.
        @param[in] next_membrane (list): New values of membrane potentials for peripheral neurons.
        @Param[in] next_active_sodium (list): New values of activation conductances of the sodium channels for peripheral neurons.
        @param[in] next_inactive_sodium (list): New values of inactivaton conductances of the sodium channels for peripheral neurons.
        @param[in] next_active_potassium (list): New values of activation conductances of the potassium channel for peripheral neurons.
        
        """
        
        self._membrane_potential = next_membrane[:];
        self._active_cond_sodium = next_active_sodium[:];
        self._inactive_cond_sodium = next_inactive_sodium[:];
        self._active_cond_potassium = next_active_potassium[:];
        
        for index in range(0, self._num_osc):
            if (self._pulse_generation[index] is False):
                if (self._membrane_potential[index] >= 0.0):
                    self._pulse_generation[index] = True;
                    self._pulse_generation_time[index].append(t);
            elif (self._membrane_potential[index] < 0.0):
                self._pulse_generation[index] = False;
            
            # Update connection from CN2 to PN
            if (self._link_weight3[index] == 0.0):
                if (self._membrane_potential[index] > self._params.threshold):
                    self._link_pulse_counter[index] += step;
                
                    if (self._link_pulse_counter[index] >= 1 / self._params.eps):
                        self._link_weight3[index] = self._params.w3;
                        self._link_activation_time[index] = t;
            elif ( not ((self._link_activation_time[index] < t) and (t < self._link_activation_time[index] + self._params.deltah)) ):
                self._link_weight3[index] = 0.0;
                self._link_pulse_counter[index] = 0.0;