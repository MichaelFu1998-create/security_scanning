def __get_nearest_feature(self, point, feature_collection):
        """!
        @brief Find nearest entry for specified point.
        
        @param[in] point (list): Pointer to point from input dataset.
        @param[in] feature_collection (list): Feature collection that is used for obtaining nearest feature for the specified point.
        
        @return (double, uint) Tuple of distance to nearest entry to the specified point and index of that entry.
        
        """
        
        minimum_distance = float("Inf");
        index_nearest_feature = -1;
        
        for index_entry in range(0, len(feature_collection)):
            point_entry = cfentry(1, linear_sum([ point ]), square_sum([ point ]));
            
            distance = feature_collection[index_entry].get_distance(point_entry, self.__measurement_type);
            if (distance < minimum_distance):
                minimum_distance = distance;
                index_nearest_feature = index_entry;
                
        return (minimum_distance, index_nearest_feature);