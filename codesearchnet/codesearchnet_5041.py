def __neuron_evolution(self, index):
        """!
        @brief Calculates state of the neuron with specified index.
        
        @param[in] index (uint): Index of neuron in the network.
        
        @return (double) New output of the specified neuron.
        
        """
        value = 0.0
        
        for index_neighbor in range(self.__num_osc):
            value += self.__weights[index][index_neighbor] * (1.0 - 2.0 * (self.__output[index_neighbor] ** 2))
        
        return value / self.__weights_summary[index]