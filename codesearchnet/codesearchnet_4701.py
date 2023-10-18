def __synchronization_mechanism(self, amplitude, index):
        """!
        @brief Calculate synchronization part using Kuramoto synchronization mechanism.
        
        @param[in] amplitude (double): Current amplitude of oscillator.
        @param[in] index (uint): Oscillator index whose synchronization influence is calculated.
        
        @return (double) Synchronization influence for the specified oscillator.
        
        """
        
        sync_influence = 0.0;
        
        for k in range(self._num_osc):
            if self.has_connection(index, k) is True:
                amplitude_neighbor = numpy.array(self.__amplitude[k], dtype = numpy.complex128, ndmin = 1);
                sync_influence += amplitude_neighbor - amplitude;
        
        return sync_influence * self.__coupling_strength / self._num_osc;