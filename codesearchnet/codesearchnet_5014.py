def __update_clusters(self):
        """!
        @brief Calculate distance to each point from the each cluster. 
        @details Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters where each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[self.__medoid_indexes[i]] for i in range(len(self.__medoid_indexes))]
        for index_point in range(len(self.__pointer_data)):
            if index_point in self.__medoid_indexes:
                continue

            index_optim = -1
            dist_optim = float('Inf')
            
            for index in range(len(self.__medoid_indexes)):
                dist = self.__distance_calculator(index_point, self.__medoid_indexes[index])
                
                if dist < dist_optim:
                    index_optim = index
                    dist_optim = dist
            
            clusters[index_optim].append(index_point)
        
        return clusters