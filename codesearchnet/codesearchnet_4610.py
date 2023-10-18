def __update_clusters(self, medoids):
        """!
        @brief Forms cluster in line with specified medoids by calculation distance from each point to medoids. 
        
        """
        
        self.__belong = [0] * len(self.__pointer_data)
        self.__clusters = [[] for i in range(len(medoids))]
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1
            dist_optim = 0.0
             
            for index in range(len(medoids)):
                dist = euclidean_distance_square(self.__pointer_data[index_point], self.__pointer_data[medoids[index]])
                 
                if (dist < dist_optim) or (index is 0):
                    index_optim = index
                    dist_optim = dist

            self.__clusters[index_optim].append(index_point)
            self.__belong[index_point] = index_optim
        
        # If cluster is not able to capture object it should be removed
        self.__clusters = [cluster for cluster in self.__clusters if len(cluster) > 0]