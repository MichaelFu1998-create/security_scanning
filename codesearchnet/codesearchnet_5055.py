def __calculate_memory_order(self, pattern):
        """!
        @brief Calculates function of the memorized pattern without any pattern validation.
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        
        @return (double) Order of memory for the specified pattern.
                
        """
        
        memory_order = 0.0;
        for index in range(len(self)):
            memory_order += pattern[index] * cmath.exp( 1j * self._phases[index] );
        
        memory_order /= len(self);
        return abs(memory_order);