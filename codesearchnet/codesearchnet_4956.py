def allocate_time_signal(self):
        """!
        @brief Analyses output dynamic and calculates time signal (signal vector information) of network output.
           
        @return (list) Time signal of network output.
        
        """
        
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_allocate_time_signal(self.__ccore_pcnn_dynamic_pointer)
        
        signal_vector_information = []
        for t in range(0, len(self.__dynamic)):
            signal_vector_information.append(sum(self.__dynamic[t]))
        
        return signal_vector_information