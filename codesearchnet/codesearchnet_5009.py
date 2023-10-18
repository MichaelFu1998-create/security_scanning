def _phase_normalization(self, teta):
        """!
        @brief Normalization of phase of oscillator that should be placed between [0; 2 * pi].
        
        @param[in] teta (double): phase of oscillator.
        
        @return (double) Normalized phase.
        
        """

        norm_teta = teta;
        while (norm_teta > (2.0 * pi)) or (norm_teta < 0):
            if (norm_teta > (2.0 * pi)):
                norm_teta -= 2.0 * pi;
            else:
                norm_teta += 2.0 * pi;
        
        return norm_teta;