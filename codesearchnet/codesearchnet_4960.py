def simulate(self, steps, stimulus):
        """!
        @brief Performs static simulation of pulse coupled neural network using.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] stimulus (list): Stimulus for oscillators, number of stimulus should be equal to number of oscillators.
        
        @return (pcnn_dynamic) Dynamic of oscillatory network - output of each oscillator on each step of simulation.
        
        """
        
        if len(stimulus) != len(self):
            raise NameError('Number of stimulus should be equal to number of oscillators. Each stimulus corresponds to only one oscillators.')
        
        if self.__ccore_pcnn_pointer is not None:
            ccore_instance_dynamic = wrapper.pcnn_simulate(self.__ccore_pcnn_pointer, steps, stimulus)
            return pcnn_dynamic(None, ccore_instance_dynamic)
        
        dynamic = []
        dynamic.append(self._outputs)
        
        for step in range(1, steps, 1):
            self._outputs = self._calculate_states(stimulus)
            
            dynamic.append(self._outputs)
        
        return pcnn_dynamic(dynamic)