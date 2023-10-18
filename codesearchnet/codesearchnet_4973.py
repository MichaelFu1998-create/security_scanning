def simulate(self, input_pattern):
        """!
        @brief Processes input pattern (no learining) and returns index of neuron-winner.
               Using index of neuron winner catched object can be obtained using property capture_objects.
               
        @param[in] input_pattern (list): Input pattern.
        
        @return (uint) Returns index of neuron-winner.
               
        @see capture_objects
        
        """

        if self.__ccore_som_pointer is not None:
            return wrapper.som_simulate(self.__ccore_som_pointer, input_pattern)
            
        return self._competition(input_pattern)