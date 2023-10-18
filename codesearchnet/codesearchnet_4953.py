def time(self):
        """!
        @brief (list) Returns sampling times when dynamic is measured during simulation.
        
        """
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_get_time(self.__ccore_pcnn_dynamic_pointer)
        
        return list(range(len(self)))