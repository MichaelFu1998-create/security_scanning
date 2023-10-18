def _legion_state_simplify(self, inputs, t, argv):
        """!
        @brief Returns new values of excitatory and inhibitory parts of oscillator of oscillator.
        @details Simplify model doesn't consider oscillator potential.
        
        @param[in] inputs (list): Initial values (current) of oscillator [excitatory, inhibitory].
        @param[in] t (double): Current time of simulation.
        @param[in] argv (uint): Extra arguments that are not used for integration - index of oscillator.
        
        @return (list) New values of excitatoty and inhibitory part of oscillator (not assign).
        
        """
        
        index = argv;
        
        x = inputs[0];  # excitatory
        y = inputs[1];  # inhibitory
        
        dx = 3.0 * x - x ** 3.0 + 2.0 - y + self._stimulus[index] + self._coupling_term[index] + self._noise[index];
        dy = self._params.eps * (self._params.gamma * (1.0 + math.tanh(x / self._params.betta)) - y);
        
        neighbors = self.get_neighbors(index);
        potential = 0.0;
        
        for index_neighbor in neighbors:
            potential += self._params.T * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
        
        return [dx, dy];