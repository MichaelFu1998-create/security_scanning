def awards(self):
        """!
        @brief Return amount of captured objects by each neuron after training.

        @return (list) Amount of captured objects by each neuron.

        @see train()
        
        """
        
        if self.__ccore_som_pointer is not None:
            self._award = wrapper.som_get_awards(self.__ccore_som_pointer)
        
        return self._award