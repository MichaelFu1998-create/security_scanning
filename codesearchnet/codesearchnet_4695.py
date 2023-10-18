def extract_number_oscillations(self, index, amplitude_threshold):
        """!
        @brief Extracts number of oscillations of specified oscillator.
        
        @param[in] index (uint): Index of oscillator whose dynamic is considered.
        @param[in] amplitude_threshold (double): Amplitude threshold when oscillation is taken into account, for example,
                    when oscillator amplitude is greater than threshold then oscillation is incremented.
        
        @return (uint) Number of oscillations of specified oscillator.
        
        """
        
        return pyclustering.utils.extract_number_oscillations(self.__amplitude, index, amplitude_threshold);