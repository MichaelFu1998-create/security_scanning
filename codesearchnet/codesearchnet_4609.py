def process(self):
        """!
        @brief Performs cluster analysis in line with rules of CLARANS algorithm.
        
        @see get_clusters()
        @see get_medoids()
        
        """
        
        random.seed()
        
        for _ in range(0, self.__numlocal):
            # set (current) random medoids
            self.__current = random.sample(range(0, len(self.__pointer_data)), self.__number_clusters)
            
            # update clusters in line with random allocated medoids
            self.__update_clusters(self.__current)
            
            # optimize configuration
            self.__optimize_configuration()
            
            # obtain cost of current cluster configuration and compare it with the best obtained
            estimation = self.__calculate_estimation()
            if estimation < self.__optimal_estimation:
                self.__optimal_medoids = self.__current[:]
                self.__optimal_estimation = estimation
        
        self.__update_clusters(self.__optimal_medoids)