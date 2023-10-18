def output(self):
        """!
        @brief (list) Returns oscillato outputs during simulation.
        
        """
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_get_output(self.__ccore_pcnn_dynamic_pointer)
            
        return self.__dynamic