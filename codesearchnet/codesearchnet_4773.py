def get_nearest_index_entry(self, entry, type_measurement):
        """!
        @brief Find nearest index of nearest entry of node for the specified entry.
        
        @param[in] entry (cfentry): Entry that is used for calculation distance.
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining nearest entry to the specified.
        
        @return (uint) Index of nearest entry of node for the specified entry.
        
        """
        
        minimum_distance = float('Inf');
        nearest_index = 0;
        
        for candidate_index in range(0, len(self.entries)):
            candidate_distance = self.entries[candidate_index].get_distance(entry, type_measurement);
            if (candidate_distance < minimum_distance):
                nearest_index = candidate_index;
        
        return nearest_index;