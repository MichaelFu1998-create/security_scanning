def __find_nearest_cluster_features(self):
        """!
        @brief Find pair of nearest CF entries.
        
        @return (list) List of two nearest enties that are represented by list [index_point1, index_point2].
        
        """
        
        minimum_distance = float("Inf");
        index1 = 0;
        index2 = 0;
        
        for index_candidate1 in range(0, len(self.__features)):
            feature1 = self.__features[index_candidate1];
            for index_candidate2 in range(index_candidate1 + 1, len(self.__features)):
                feature2 = self.__features[index_candidate2];
                
                distance = feature1.get_distance(feature2, self.__measurement_type);
                if (distance < minimum_distance):
                    minimum_distance = distance;
                    
                    index1 = index_candidate1;
                    index2 = index_candidate2;
        
        return [index1, index2];