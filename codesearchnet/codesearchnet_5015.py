def __update_medoids(self):
        """!
        @brief Find medoids of clusters in line with contained objects.
        
        @return (list) list of medoids for current number of clusters.
        
        """

        medoid_indexes = [-1] * len(self.__clusters)
        
        for index in range(len(self.__clusters)):
            medoid_index = medoid(self.__pointer_data, self.__clusters[index], metric=self.__metric, data_type=self.__data_type)
            medoid_indexes[index] = medoid_index
             
        return medoid_indexes