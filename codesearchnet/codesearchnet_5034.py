def allocate_observation_matrix(self):
        """!
        @brief Allocates observation matrix in line with output dynamic of the network.
        @details Matrix where state of each neuron is denoted by zero/one in line with Heaviside function on each iteration.
        
        @return (list) Observation matrix of the network dynamic.
        
        """
        number_neurons = len(self.output[0])
        observation_matrix = []
        
        for iteration in range(len(self.output)):
            obervation_column = []
            for index_neuron in range(number_neurons):
                obervation_column.append(heaviside(self.output[iteration][index_neuron]))
            
            observation_matrix.append(obervation_column)
        
        return observation_matrix