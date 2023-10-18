def __calculate_amplitude(self, amplitude, t, argv):
        """!
        @brief Returns new amplitude value for particular oscillator that is defined by index that is in 'argv' argument.
        @details The method is used for differential calculation.
        
        @param[in] amplitude (double): Current amplitude of oscillator.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (uint): Index of the current oscillator.
        
        @return (double) New amplitude of the oscillator.
        
        """
        
        z = amplitude.view(numpy.complex);
        dzdt = self.__landau_stuart(z, argv) + self.__synchronization_mechanism(z, argv);
        
        return dzdt.view(numpy.float64);