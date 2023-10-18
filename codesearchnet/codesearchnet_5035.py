def __allocate_neuron_patterns(self, start_iteration, stop_iteration):
        """!
        @brief Allocates observation transposed matrix of neurons that is limited by specified periods of simulation.
        @details Matrix where state of each neuron is denoted by zero/one in line with Heaviside function on each iteration.
        
        @return (list) Transposed observation matrix that is limited by specified periods of simulation.
        
        """
        
        pattern_matrix = []
        for index_neuron in range(len(self.output[0])):
            pattern_neuron = []
            for iteration in range(start_iteration, stop_iteration):
                pattern_neuron.append(heaviside(self.output[iteration][index_neuron]))
            
            pattern_matrix.append(pattern_neuron)
        
        return pattern_matrix