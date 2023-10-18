def __update_clusters(self):
        """!
        @brief Calculate Manhattan distance to each point from the each cluster. 
        @details Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters where each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for i in range(len(self.__medians))]
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1
            dist_optim = 0.0
             
            for index in range(len(self.__medians)):
                dist = self.__metric(self.__pointer_data[index_point], self.__medians[index])
                 
                if (dist < dist_optim) or (index == 0):
                    index_optim = index
                    dist_optim = dist
             
            clusters[index_optim].append(index_point)
            
        # If cluster is not able to capture object it should be removed
        clusters = [cluster for cluster in clusters if len(cluster) > 0]
        
        return clusters