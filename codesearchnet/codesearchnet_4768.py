def get_nearest_successors(self, type_measurement):
        """!
        @brief Find pair of nearest successors of the node in line with measurement type.
        
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining nearest successors.
        
        @return (list) Pair of nearest successors represented by list.
        
        """
                
        nearest_node1 = None;
        nearest_node2 = None;
        nearest_distance = float("Inf");
        
        for i in range(0, len(self.successors)):
            candidate1 = self.successors[i];
            
            for j in range(i + 1, len(self.successors)):
                candidate2 = self.successors[j];
                candidate_distance = candidate1.get_distance(candidate2, type_measurement);
                
                if (candidate_distance < nearest_distance):
                    nearest_distance = candidate_distance;
                    nearest_node1 = candidate1;
                    nearest_node2 = candidate2;
        
        return [nearest_node1, nearest_node2];