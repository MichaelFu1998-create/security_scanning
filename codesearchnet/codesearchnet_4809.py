def output(self):
        """!
        @brief Returns output dynamic of the network.
        
        """
        if (self.__ccore_legion_dynamic_pointer is not None):
            return wrapper.legion_dynamic_get_output(self.__ccore_legion_dynamic_pointer);
            
        return self.__output;