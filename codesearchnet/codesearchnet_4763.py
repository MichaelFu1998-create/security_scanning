def get_distance(self, node, type_measurement):
        """!
        @brief Calculates distance between nodes in line with specified type measurement.
        
        @param[in] node (cfnode): CF-node that is used for calculation distance to the current node.
        @param[in] type_measurement (measurement_type): Measurement type that is used for calculation distance.
        
        @return (double) Distance between two nodes.
        
        """
        
        return self.feature.get_distance(node.feature, type_measurement);