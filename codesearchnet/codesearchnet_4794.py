def __merge_by_signle_link(self):
        """!
        @brief Merges the most similar clusters in line with single link type.
        
        """
        
        minimum_single_distance = float('Inf');
        indexes = None;
        
        for index_cluster1 in range(0, len(self.__clusters)):
            for index_cluster2 in range(index_cluster1 + 1, len(self.__clusters)):
                candidate_minimum_distance = self.__calculate_nearest_distance(index_cluster1, index_cluster2);
                
                if (candidate_minimum_distance < minimum_single_distance):
                    minimum_single_distance = candidate_minimum_distance;
                    indexes = [index_cluster1, index_cluster2];

        self.__clusters[indexes[0]] += self.__clusters[indexes[1]];  
        self.__clusters.pop(indexes[1]);