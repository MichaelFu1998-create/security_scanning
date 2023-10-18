def get_farthest_successors(self, type_measurement):
        """!
        @brief Find pair of farthest successors of the node in line with measurement type.
        
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining farthest successors.
        
        @return (list) Pair of farthest successors represented by list [cfnode1, cfnode2].
        
        """
        
        farthest_node1 = None;
        farthest_node2 = None;
        farthest_distance = 0;
        
        for i in range(0, len(self.successors)):
            candidate1 = self.successors[i];
            
            for j in range(i + 1, len(self.successors)):
                candidate2 = self.successors[j];
                candidate_distance = candidate1.get_distance(candidate2, type_measurement);
                
                if (candidate_distance > farthest_distance):
                    farthest_distance = candidate_distance;
                    farthest_node1 = candidate1;
                    farthest_node2 = candidate2;        
        
                    return [farthest_node1, farthest_node2];