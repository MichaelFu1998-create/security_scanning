def __calculate_links(self, cluster1, cluster2):
        """!
        @brief Returns number of link between two clusters. 
        @details Link between objects (points) exists only if distance between them less than connectivity radius.
        
        @param[in] cluster1 (list): The first cluster.
        @param[in] cluster2 (list): The second cluster.
        
        @return (uint) Number of links between two clusters.
        
        """
        
        number_links = 0;
        
        for index1 in cluster1:
            for index2 in cluster2:
                number_links += self.__adjacency_matrix[index1][index2];
                
        return number_links;