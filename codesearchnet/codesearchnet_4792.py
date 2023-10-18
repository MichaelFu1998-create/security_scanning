def __merge_by_complete_link(self):
        """!
        @brief Merges the most similar clusters in line with complete link type.
        
        """
        
        minimum_complete_distance = float('Inf');
        indexes = None;
        
        for index_cluster1 in range(0, len(self.__clusters)):
            for index_cluster2 in range(index_cluster1 + 1, len(self.__clusters)):
                candidate_maximum_distance = self.__calculate_farthest_distance(index_cluster1, index_cluster2);
                
                if (candidate_maximum_distance < minimum_complete_distance):
                    minimum_complete_distance = candidate_maximum_distance;
                    indexes = [index_cluster1, index_cluster2];

        self.__clusters[indexes[0]] += self.__clusters[indexes[1]];  
        self.__clusters.pop(indexes[1]);