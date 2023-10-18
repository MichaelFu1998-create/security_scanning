def _phase_kuramoto(self, teta, t, argv):
        """!
        @brief Returns result of phase calculation for oscillator in the network.
        
        @param[in] teta (double): Value of phase of the oscillator with index argv in the network.
        @param[in] t (double): Unused, can be ignored.
        @param[in] argv (uint): Index of the oscillator in the network.
        
        @return (double) New value of phase for oscillator with index argv.
        
        """
        
        index = argv;
        phase = 0;
        
        for k in range(0, self._num_osc):
            if (self.has_connection(index, k) == True):
                phase += self._negative_weight * math.sin(self._phases[k] - teta);
            else:
                phase += self._positive_weight * math.sin(self._phases[k] - teta);
            
        return ( phase / self._reduction );