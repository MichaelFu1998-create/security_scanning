def weights(self):
        """!
        @brief Return weight of each neuron.

        @return (list) Weights of each neuron.
        
        """
        
        if self.__ccore_som_pointer is not None:
            self._weights = wrapper.som_get_weights(self.__ccore_som_pointer)
        
        return self._weights