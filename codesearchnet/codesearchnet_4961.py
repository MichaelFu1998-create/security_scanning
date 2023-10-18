def _calculate_states(self, stimulus):
        """!
        @brief Calculates states of oscillators in the network for current step and stored them except outputs of oscillators.
        
        @param[in] stimulus (list): Stimulus for oscillators, number of stimulus should be equal to number of oscillators.
        
        @return (list) New outputs for oscillators (do not stored it).
        
        """
        
        feeding = [0.0] * self._num_osc
        linking = [0.0] * self._num_osc
        outputs = [0.0] * self._num_osc
        threshold = [0.0] * self._num_osc
        
        for index in range(0, self._num_osc, 1):
            neighbors = self.get_neighbors(index)
            
            feeding_influence = 0.0
            linking_influence = 0.0
            
            for index_neighbour in neighbors:
                feeding_influence += self._outputs[index_neighbour] * self._params.M
                linking_influence += self._outputs[index_neighbour] * self._params.W
            
            feeding_influence *= self._params.VF
            linking_influence *= self._params.VL
            
            feeding[index] = self._params.AF * self._feeding[index] + stimulus[index] + feeding_influence
            linking[index] = self._params.AL * self._linking[index] + linking_influence
            
            # calculate internal activity
            internal_activity = feeding[index] * (1.0 + self._params.B * linking[index])
            
            # calculate output of the oscillator
            if internal_activity > self._threshold[index]:
                outputs[index] = self.__OUTPUT_TRUE
            else:
                outputs[index] = self.__OUTPUT_FALSE
            
            # In case of Fast Linking we should calculate threshold until output is changed.
            if self._params.FAST_LINKING is not True:
                threshold[index] = self._params.AT * self._threshold[index] + self._params.VT * outputs[index]

        # In case of Fast Linking we need to wait until output is changed.
        if self._params.FAST_LINKING is True:
            output_change = True    # Set it True for the for the first iteration.
            previous_outputs = outputs[:]

            while output_change is True:
                current_output_change = False

                for index in range(0, self._num_osc, 1):
                    linking_influence = 0.0

                    neighbors = self.get_neighbors(index)
                    for index_neighbour in neighbors:
                        linking_influence += previous_outputs[index_neighbour] * self._params.W
                    
                    linking_influence *= self._params.VL
                    linking[index] = linking_influence
                    
                    internal_activity = feeding[index] * (1.0 + self._params.B * linking[index])
                    
                    # calculate output of the oscillator
                    if internal_activity > self._threshold[index]:
                        outputs[index] = self.__OUTPUT_TRUE
                    else:
                        outputs[index] = self.__OUTPUT_FALSE

                    current_output_change |= (outputs[index] != previous_outputs[index])
                
                output_change = current_output_change
                
                if output_change is True:
                    previous_outputs = outputs[:]
        
        # In case of Fast Linking threshold should be calculated after fast linking.
        if self._params.FAST_LINKING is True:
            for index in range(0, self._num_osc, 1):
                threshold[index] = self._params.AT * self._threshold[index] + self._params.VT * outputs[index]
        
        self._feeding = feeding[:]
        self._linking = linking[:]
        self._threshold = threshold[:]
        
        return outputs