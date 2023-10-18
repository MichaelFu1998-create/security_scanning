def get_farthest_entries(self, type_measurement):
        """!
        @brief Find pair of farthest entries of the node.
        
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining farthest entries.
        
        @return (list) Pair of farthest entries of the node that are represented by list.
        
        """
        
        farthest_entity1 = None;
        farthest_entity2 = None;
        farthest_distance = 0;
        
        for i in range(0, len(self.entries)):
            candidate1 = self.entries[i];
            
            for j in range(i + 1, len(self.entries)):
                candidate2 = self.entries[j];
                candidate_distance = candidate1.get_distance(candidate2, type_measurement);
                
                if (candidate_distance > farthest_distance):
                    farthest_distance = candidate_distance;
                    farthest_entity1 = candidate1;
                    farthest_entity2 = candidate2;
        
        return [farthest_entity1, farthest_entity2];