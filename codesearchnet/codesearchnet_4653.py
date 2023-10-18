def __decode_data(self):
        """!
        @brief Decodes data from CF-tree features.
        
        """
        
        self.__clusters = [ [] for _ in range(self.__number_clusters) ];
        self.__noise = [];
        
        for index_point in range(0, len(self.__pointer_data)):
            (_, cluster_index) = self.__get_nearest_feature(self.__pointer_data[index_point], self.__features);
            
            self.__clusters[cluster_index].append(index_point);