def __calculate_farthest_distance(self, index_cluster1, index_cluster2):
        """!
        @brief Finds two farthest objects in two specified clusters in terms and returns distance between them.
        
        @param[in] (uint) Index of the first cluster.
        @param[in] (uint) Index of the second cluster.
        
        @return The farthest euclidean distance between two clusters.
        
        """
        candidate_maximum_distance = 0.0;
        for index_object1 in self.__clusters[index_cluster1]:
            for index_object2 in self.__clusters[index_cluster2]:
                distance = euclidean_distance_square(self.__pointer_data[index_object1], self.__pointer_data[index_object2]);
                
                if (distance > candidate_maximum_distance):
                    candidate_maximum_distance = distance;
    
        return candidate_maximum_distance;