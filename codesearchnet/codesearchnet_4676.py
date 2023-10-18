def __calculate_initial_clusters(self, centers):
        """!
        @brief Calculate Euclidean distance to each point from the each cluster. 
        @brief Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters. Each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for _ in range(len(centers))]
        for index_point in range(len(self.__sample)):
            index_optim, dist_optim = -1, 0.0
             
            for index in range(len(centers)):
                dist = euclidean_distance_square(self.__sample[index_point], centers[index])
                 
                if (dist < dist_optim) or (index is 0):
                    index_optim, dist_optim = index, dist
             
            clusters[index_optim].append(index_point)
        
        return clusters