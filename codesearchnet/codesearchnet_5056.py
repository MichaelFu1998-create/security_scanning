def _phase_kuramoto(self, teta, t, argv):
        """!
        @brief Returns result of phase calculation for specified oscillator in the network.
        
        @param[in] teta (double): Phase of the oscillator that is differentiated.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): Index of the oscillator in the list.
        
        @return (double) New phase for specified oscillator (don't assign it here).
        
        """
        
        index = argv;
        
        phase = 0.0;
        term = 0.0;
        
        for k in range(0, self._num_osc):
            if (k != index):
                phase_delta = self._phases[k] - teta;
                
                phase += self._coupling[index][k] * math.sin(phase_delta);
                
                term1 = self._increase_strength1 * math.sin(2.0 * phase_delta);
                term2 = self._increase_strength2 * math.sin(3.0 * phase_delta);
                
                term += (term1 - term2);
                
        return ( phase + term / len(self) );