def __merge_by_average_link(self):
        """!
        @brief Merges the most similar clusters in line with average link type.
        
        """
        
        minimum_average_distance = float('Inf');
        
        for index_cluster1 in range(0, len(self.__clusters)):
            for index_cluster2 in range(index_cluster1 + 1, len(self.__clusters)):
                
                # Find farthest objects
                candidate_average_distance = 0.0;
                for index_object1 in self.__clusters[index_cluster1]:
                    for index_object2 in self.__clusters[index_cluster2]:
                        candidate_average_distance += euclidean_distance_square(self.__pointer_data[index_object1], self.__pointer_data[index_object2]);
                
                candidate_average_distance /= (len(self.__clusters[index_cluster1]) + len(self.__clusters[index_cluster2]));
                
                if (candidate_average_distance < minimum_average_distance):
                    minimum_average_distance = candidate_average_distance;
                    indexes = [index_cluster1, index_cluster2];
        
        self.__clusters[indexes[0]] += self.__clusters[indexes[1]];  
        self.__clusters.pop(indexes[1]);