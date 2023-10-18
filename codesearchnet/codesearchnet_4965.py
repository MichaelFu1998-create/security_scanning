def capture_objects(self):
        """!
        @brief Returns indexes of captured objects by each neuron.
        @details For example, network with size 2x2 has been trained on 5 sample, we neuron #1 has won one object with
                  index '1', neuron #2 - objects with indexes '0', '3', '4', neuron #3 - nothing, neuron #4 - object
                  with index '2'. Thus, output is [ [1], [0, 3, 4], [], [2] ].

        @return (list) Indexes of captured objects by each neuron.
        
        """
        
        if self.__ccore_som_pointer is not None:
            self._capture_objects = wrapper.som_get_capture_objects(self.__ccore_som_pointer)
        
        return self._capture_objects