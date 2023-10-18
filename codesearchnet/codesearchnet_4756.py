def get_distance(self, entry, type_measurement):
        """!
        @brief Calculates distance between two clusters in line with measurement type.
        
        @details In case of usage CENTROID_EUCLIDIAN_DISTANCE square euclidian distance will be returned.
                 Square root should be taken from the result for obtaining real euclidian distance between
                 entries. 
        
        @param[in] entry (cfentry): Clustering feature to which distance should be obtained.
        @param[in] type_measurement (measurement_type): Distance measurement algorithm between two clusters.
        
        @return (double) Distance between two clusters.
        
        """
        
        if (type_measurement is measurement_type.CENTROID_EUCLIDEAN_DISTANCE):
            return euclidean_distance_square(entry.get_centroid(), self.get_centroid());
        
        elif (type_measurement is measurement_type.CENTROID_MANHATTAN_DISTANCE):
            return manhattan_distance(entry.get_centroid(), self.get_centroid());
        
        elif (type_measurement is measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE):
            return self.__get_average_inter_cluster_distance(entry);
            
        elif (type_measurement is measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE):
            return self.__get_average_intra_cluster_distance(entry);
        
        elif (type_measurement is measurement_type.VARIANCE_INCREASE_DISTANCE):
            return self.__get_variance_increase_distance(entry);
        
        else:
            assert 0;