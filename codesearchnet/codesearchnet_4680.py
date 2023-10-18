def process(self):
        """!
        @brief Run clustering process of the algorithm.
        @details This method should be called before call 'get_clusters()'.
        
        """
        
        previous_likelihood = -200000
        current_likelihood = -100000
        
        current_iteration = 0
        while(self.__stop is False) and (abs(previous_likelihood - current_likelihood) > self.__tolerance) and (current_iteration < self.__iterations):
            self.__expectation_step()
            self.__maximization_step()
            
            current_iteration += 1
            
            self.__extract_clusters()
            self.__notify()
            
            previous_likelihood = current_likelihood
            current_likelihood = self.__log_likelihood()
            self.__stop = self.__get_stop_condition()
        
        self.__normalize_probabilities()