def get_centroid(self):
        """!
        @brief Calculates centroid of cluster that is represented by the entry. 
        @details It's calculated once when it's requested after the last changes.
        
        @return (list) Centroid of cluster that is represented by the entry.
        
        """
        
        if (self.__centroid is not None):
            return self.__centroid;
        
        self.__centroid = [0] * len(self.linear_sum);
        for index_dimension in range(0, len(self.linear_sum)):
            self.__centroid[index_dimension] = self.linear_sum[index_dimension] / self.number_points;
        
        return self.__centroid;