def _neuron_states(self, inputs, t, argv):
        """!
        @brief Returns new value of the neuron (oscillator).
        
        @param[in] inputs (list): Initial values (current) of the neuron - excitatory.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): Extra arguments that are not used for integration - index of the neuron.
        
        @return (double) New value of the neuron.
        
        """
        
        xi = inputs[0];
        index = argv;
        
        # own impact
        impact = self._weight[index][index] * self._outputs[index];
        
        for i in range(0, self._num_osc, 1):
            if (self.has_connection(i, index)):
                impact += self._weight[index][i] * self._outputs[i];

        x = -xi + impact;
                
        if (xi > 1): self._outputs_buffer[index] = 1; 
        if (xi < -1): self._outputs_buffer[index] = -1;
       
        return x;