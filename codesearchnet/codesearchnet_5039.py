def simulate(self, steps, stimulus):
        """!
        @brief Simulates chaotic neural network with extrnal stimulus during specified steps.
        @details Stimulus are considered as a coordinates of neurons and in line with that weights
                 are initialized.
        
        @param[in] steps (uint): Amount of steps for simulation.
        @param[in] stimulus (list): Stimulus that are used for simulation.
        
        @return (cnn_dynamic) Output dynamic of the chaotic neural network.
        
        """
        
        self.__create_weights(stimulus)
        self.__location = stimulus
        
        dynamic = cnn_dynamic([], [])
        dynamic.output.append(self.__output)
        dynamic.time.append(0)
        
        for step in range(1, steps, 1):
            self.__output = self.__calculate_states()
            
            dynamic.output.append(self.__output)
            dynamic.time.append(step)
            
        return dynamic