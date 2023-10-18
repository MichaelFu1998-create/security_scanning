def notify(self, means, covariances, clusters):
        """!
        @brief This method is used by the algorithm to notify observer about changes where the algorithm
                should provide new values: means, covariances and allocated clusters.
        
        @param[in] means (list): Mean of each cluster on currect step.
        @param[in] covariances (list): Covariances of each cluster on current step.
        @param[in] clusters (list): Allocated cluster on current step.
        
        """
        self.__means_evolution.append(means)
        self.__covariances_evolution.append(covariances)
        self.__clusters_evolution.append(clusters)