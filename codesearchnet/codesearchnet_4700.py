def __landau_stuart(self, amplitude, index):
        """!
        @brief Calculate Landau-Stuart state.
        
        @param[in] amplitude (double): Current amplitude of oscillator.
        @param[in] index (uint): Oscillator index whose state is calculated. 
        
        @return (double) Landau-Stuart state.
        
        """
        
        return (self.__properties[index] - numpy.absolute(amplitude) ** 2) * amplitude;