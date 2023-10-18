def memory_order(self, pattern):
        """!
        @brief Calculates function of the memorized pattern.
        @details Throws exception if length of pattern is not equal to size of the network or if it consists feature with value that are not equal to [-1; 1].
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        
        @return (double) Order of memory for the specified pattern.
        
        """
        
        self.__validate_pattern(pattern);
        
        if (self._ccore_network_pointer is not None):
            return wrapper.syncpr_memory_order(self._ccore_network_pointer, pattern);
        
        else:
            return self.__calculate_memory_order(pattern);