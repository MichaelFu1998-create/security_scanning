def time(self):
        """!
        @brief Returns simulation time.
        
        """
        if (self.__ccore_legion_dynamic_pointer is not None):
            return wrapper.legion_dynamic_get_time(self.__ccore_legion_dynamic_pointer);
        
        return list(range(len(self)));