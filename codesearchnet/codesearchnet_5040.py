def __calculate_states(self):
        """!
        @brief Calculates new state of each neuron.
        @detail There is no any assignment.
        
        @return (list) Returns new states (output).
        
        """
        
        output = [ 0.0 for _ in range(self.__num_osc) ]
        
        for i in range(self.__num_osc):
            output[i] = self.__neuron_evolution(i)
        
        return output