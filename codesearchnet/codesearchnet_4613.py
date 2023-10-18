def __calculate_estimation(self):
        """!
        @brief Calculates estimation (cost) of the current clusters. The lower the estimation,
               the more optimally configuration of clusters.
        
        @return (double) estimation of current clusters.
        
        """
        estimation = 0.0
        for index_cluster in range(0, len(self.__clusters)):
            cluster = self.__clusters[index_cluster]
            index_medoid = self.__current[index_cluster]
            for index_point in cluster:
                estimation += euclidean_distance_square(self.__pointer_data[index_point], self.__pointer_data[index_medoid])
        
        return estimation