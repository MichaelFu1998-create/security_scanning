def process(self):
        """!
        @brief Performs cluster analysis in line with rules of BIRCH algorithm.
        
        @remark Results of clustering can be obtained using corresponding gets methods.
        
        @see get_clusters()
        
        """
        
        self.__insert_data();
        self.__extract_features();

        # in line with specification modify hierarchical algorithm should be used for further clustering
        current_number_clusters = len(self.__features);
        
        while (current_number_clusters > self.__number_clusters):
            indexes = self.__find_nearest_cluster_features();
            
            self.__features[indexes[0]] += self.__features[indexes[1]];
            self.__features.pop(indexes[1]);
            
            current_number_clusters = len(self.__features);
            
        # decode data
        self.__decode_data();