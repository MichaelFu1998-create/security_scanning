def size(self):
        """!
        @brief Return size of self-organized map that is defined by total number of neurons.

        @return (uint) Size of self-organized map (number of neurons).
        
        """
        
        if self.__ccore_som_pointer is not None:
            self._size = wrapper.som_get_size(self.__ccore_som_pointer)
            
        return self._size