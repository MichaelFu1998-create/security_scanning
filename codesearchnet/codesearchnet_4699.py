def __oscillator_property(self, index):
        """!
        @brief Calculate Landau-Stuart oscillator constant property that is based on frequency and radius.
        
        @param[in] index (uint): Oscillator index whose property is calculated.
        
        @return (double) Oscillator property.
        
        """
        
        return numpy.array(1j * self.__frequency[index] + self.__radius[index]**2, dtype = numpy.complex128, ndmin = 1);