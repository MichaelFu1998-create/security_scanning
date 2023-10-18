def __update_medians(self):
        """!
        @brief Calculate medians of clusters in line with contained objects.
        
        @return (list) list of medians for current number of clusters.
        
        """
         
        medians = [[] for i in range(len(self.__clusters))]
         
        for index in range(len(self.__clusters)):
            medians[index] = [0.0 for i in range(len(self.__pointer_data[0]))]
            length_cluster = len(self.__clusters[index])
            
            for index_dimension in range(len(self.__pointer_data[0])):
                sorted_cluster = sorted(self.__clusters[index], key=lambda x: self.__pointer_data[x][index_dimension])
                
                relative_index_median = int(math.floor((length_cluster - 1) / 2))
                index_median = sorted_cluster[relative_index_median]
                
                if (length_cluster % 2) == 0:
                    index_median_second = sorted_cluster[relative_index_median + 1]
                    medians[index][index_dimension] = (self.__pointer_data[index_median][index_dimension] + self.__pointer_data[index_median_second][index_dimension]) / 2.0
                    
                else:
                    medians[index][index_dimension] = self.__pointer_data[index_median][index_dimension]
             
        return medians