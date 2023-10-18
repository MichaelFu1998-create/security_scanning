def process(self):
        """!
        @brief Performs cluster analysis in line with rules of agglomerative algorithm and similarity.
        
        @see get_clusters()
        
        """
        
        if (self.__ccore is True):
            self.__clusters = wrapper.agglomerative_algorithm(self.__pointer_data, self.__number_clusters, self.__similarity);

        else:
            self.__clusters = [[index] for index in range(0, len(self.__pointer_data))];
            
            current_number_clusters = len(self.__clusters);
                
            while (current_number_clusters > self.__number_clusters):
                self.__merge_similar_clusters();
                current_number_clusters = len(self.__clusters);