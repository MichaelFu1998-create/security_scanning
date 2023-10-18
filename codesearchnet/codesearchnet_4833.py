def __update_central_neurons(self, t, next_cn_membrane, next_cn_active_sodium, next_cn_inactive_sodium, next_cn_active_potassium):
        """!
        @brief Update of central neurons in line with new values of current in channels.
        
        @param[in] t (doubles): Current time of simulation.
        @param[in] next_membrane (list): New values of membrane potentials for central neurons.
        @Param[in] next_active_sodium (list): New values of activation conductances of the sodium channels for central neurons.
        @param[in] next_inactive_sodium (list): New values of inactivaton conductances of the sodium channels for central neurons.
        @param[in] next_active_potassium (list): New values of activation conductances of the potassium channel for central neurons.
        
        """
        
        for index in range(0, len(self._central_element)):
            self._central_element[index].membrane_potential = next_cn_membrane[index];
            self._central_element[index].active_cond_sodium = next_cn_active_sodium[index];
            self._central_element[index].inactive_cond_sodium = next_cn_inactive_sodium[index];
            self._central_element[index].active_cond_potassium = next_cn_active_potassium[index];
            
            if (self._central_element[index].pulse_generation is False):
                if (self._central_element[index].membrane_potential >= 0.0):
                    self._central_element[index].pulse_generation = True;
                    self._central_element[index].pulse_generation_time.append(t);
            elif (self._central_element[index].membrane_potential < 0.0):
                self._central_element[index].pulse_generation = False;