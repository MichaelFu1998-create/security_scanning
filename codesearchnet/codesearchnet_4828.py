def _phase_kuramoto(self, teta, t, argv):
        """!
        @brief Overrided method for calculation of oscillator phase.
        
        @param[in] teta (double): Current value of phase.
        @param[in] t (double): Time (can be ignored).
        @param[in] argv (uint): Index of oscillator whose phase represented by argument teta.
        
        @return (double) New value of phase of oscillator with index 'argv'.
        
        """
        
        index = argv;   # index of oscillator
        phase = 0.0;      # phase of a specified oscillator that will calculated in line with current env. states.
        
        neighbors = self.get_neighbors(index);
        for k in neighbors:
            conn_weight = 1.0;
            if (self._ena_conn_weight is True):
                conn_weight = self._conn_weight[index][k];
                
            phase += conn_weight * self._weight * math.sin(self._phases[k] - teta);
        
        divider = len(neighbors);
        if (divider == 0):
            divider = 1.0;
            
        return ( self._freq[index] + (phase / divider) );