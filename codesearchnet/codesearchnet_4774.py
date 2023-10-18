def get_nearest_entry(self, entry, type_measurement):
        """!
        @brief Find nearest entry of node for the specified entry.
        
        @param[in] entry (cfentry): Entry that is used for calculation distance.
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining nearest entry to the specified.
        
        @return (cfentry) Nearest entry of node for the specified entry.
        
        """
        
        min_key = lambda cur_entity: cur_entity.get_distance(entry, type_measurement);
        return min(self.__entries, key = min_key);