def _global_inhibitor_state(self, z, t, argv):
        """!
        @brief Returns new value of global inhibitory
        
        @param[in] z (dobule): Current value of inhibitory.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): It's not used, can be ignored.
        
        @return (double) New value if global inhibitory (not assign).
        
        """
        
        sigma = 0.0;
        
        for x in self._excitatory:
            if (x > self._params.teta_zx):
                sigma = 1.0;
                break;
        
        return self._params.fi * (sigma - z);