def __get_average_intra_cluster_distance(self, entry):
        """!
        @brief Calculates average intra cluster distance between current and specified clusters.
        
        @param[in] entry (cfentry): Clustering feature to which distance should be obtained.
        
        @return (double) Average intra cluster distance.
        
        """
        
        linear_part_first = list_math_addition(self.linear_sum, entry.linear_sum);
        linear_part_second = linear_part_first;
        
        linear_part_distance = sum(list_math_multiplication(linear_part_first, linear_part_second));
        
        general_part_distance = 2.0 * (self.number_points + entry.number_points) * (self.square_sum + entry.square_sum) - 2.0 * linear_part_distance;
        
        return (general_part_distance / ( (self.number_points + entry.number_points) * (self.number_points + entry.number_points - 1.0) )) ** 0.5;