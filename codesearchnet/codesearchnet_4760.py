def __get_average_inter_cluster_distance(self, entry):
        """!
        @brief Calculates average inter cluster distance between current and specified clusters.
        
        @param[in] entry (cfentry): Clustering feature to which distance should be obtained.
        
        @return (double) Average inter cluster distance.
        
        """
        
        linear_part_distance = sum(list_math_multiplication(self.linear_sum, entry.linear_sum));
        
        return ( (entry.number_points * self.square_sum - 2.0 * linear_part_distance + self.number_points * entry.square_sum) / (self.number_points * entry.number_points) ) ** 0.5;