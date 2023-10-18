def __calculate_goodness(self, cluster1, cluster2):
        """!
        @brief Calculates coefficient 'goodness measurement' between two clusters. The coefficient defines level of suitability of clusters for merging.
        
        @param[in] cluster1 (list): The first cluster.
        @param[in] cluster2 (list): The second cluster.
        
        @return Goodness measure between two clusters.
        
        """
        
        number_links = self.__calculate_links(cluster1, cluster2);
        devider = (len(cluster1) + len(cluster2)) ** self.__degree_normalization - len(cluster1) ** self.__degree_normalization - len(cluster2) ** self.__degree_normalization;
        
        return (number_links / devider);