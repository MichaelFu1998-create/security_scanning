def train(self, data, epochs, autostop=False):
        """!
        @brief Trains self-organized feature map (SOM).

        @param[in] data (list): Input data - list of points where each point is represented by list of features, for example coordinates.
        @param[in] epochs (uint): Number of epochs for training.        
        @param[in] autostop (bool): Automatic termination of learining process when adaptation is not occurred.
        
        @return (uint) Number of learining iterations.
        
        """
        
        self._data = data
        
        if self.__ccore_som_pointer is not None:
            return wrapper.som_train(self.__ccore_som_pointer, data, epochs, autostop)

        self._sqrt_distances = self.__initialize_distances(self._size, self._location)

        for i in range(self._size):
            self._award[i] = 0
            self._capture_objects[i].clear()
        
        # weights
        self._create_initial_weights(self._params.init_type)
        
        previous_weights = None
        
        for epoch in range(1, epochs + 1):
            # Depression term of coupling
            self._local_radius = (self._params.init_radius * math.exp(-(epoch / epochs))) ** 2
            self._learn_rate = self._params.init_learn_rate * math.exp(-(epoch / epochs))
            
            # Clear statistics
            if autostop:
                for i in range(self._size):
                    self._award[i] = 0
                    self._capture_objects[i].clear()
            
            for i in range(len(self._data)):
                # Step 1: Competition:
                index = self._competition(self._data[i])
                    
                # Step 2: Adaptation:   
                self._adaptation(index, self._data[i])
                
                # Update statistics
                if (autostop == True) or (epoch == epochs):
                    self._award[index] += 1
                    self._capture_objects[index].append(i)
            
            # Check requirement of stopping
            if autostop:
                if previous_weights is not None:
                    maximal_adaptation = self._get_maximal_adaptation(previous_weights)
                    if maximal_adaptation < self._params.adaptation_threshold:
                        return epoch
            
                previous_weights = [item[:] for item in self._weights]
        
        return epochs