def _legion_state(self, inputs, t, argv):
        """!
        @brief Returns new values of excitatory and inhibitory parts of oscillator and potential of oscillator.
        
        @param[in] inputs (list): Initial values (current) of oscillator [excitatory, inhibitory, potential].
        @param[in] t (double): Current time of simulation.
        @param[in] argv (uint): Extra arguments that are not used for integration - index of oscillator.
        
        @return (list) New values of excitatoty and inhibitory part of oscillator and new value of potential (not assign).
        
        """
        
        index = argv;
        
        x = inputs[0];  # excitatory
        y = inputs[1];  # inhibitory
        p = inputs[2];  # potential
        
        potential_influence = heaviside(p + math.exp(-self._params.alpha * t) - self._params.teta);
        
        dx = 3.0 * x - x ** 3.0 + 2.0 - y + self._stimulus[index] * potential_influence + self._coupling_term[index] + self._noise[index];
        dy = self._params.eps * (self._params.gamma * (1.0 + math.tanh(x / self._params.betta)) - y);
        
        neighbors = self.get_neighbors(index);
        potential = 0.0;
        
        for index_neighbor in neighbors:
            potential += self._params.T * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
        
        dp = self._params.lamda * (1.0 - p) * heaviside(potential - self._params.teta_p) - self._params.mu * p;
        
        return [dx, dy, dp];