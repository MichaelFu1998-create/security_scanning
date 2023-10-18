def __calculate_center(self, cluster):
        """!
        @brief Calculates new center.
        
        @return (list) New value of the center of the specified cluster.
        
        """
         
        dimension = len(self.__pointer_data[cluster[0]]);
        center = [0] * dimension;
        for index_point in cluster:
            for index_dimension in range(0, dimension):
                center[index_dimension] += self.__pointer_data[index_point][index_dimension];
         
        for index_dimension in range(0, dimension):
            center[index_dimension] /= len(cluster);
             
        return center;