def __get_variance_increase_distance(self, entry):
        """!
        @brief Calculates variance increase distance between current and specified clusters.
        
        @param[in] entry (cfentry): Clustering feature to which distance should be obtained.
        
        @return (double) Variance increase distance.
        
        """
                
        linear_part_12 = list_math_addition(self.linear_sum, entry.linear_sum);
        variance_part_first = (self.square_sum + entry.square_sum) - \
            2.0 * sum(list_math_multiplication(linear_part_12, linear_part_12)) / (self.number_points + entry.number_points) + \
            (self.number_points + entry.number_points) * sum(list_math_multiplication(linear_part_12, linear_part_12)) / (self.number_points + entry.number_points)**2.0;

        
        linear_part_11 = sum(list_math_multiplication(self.linear_sum, self.linear_sum));
        variance_part_second = -( self.square_sum - (2.0 * linear_part_11 / self.number_points) + (linear_part_11 / self.number_points) );
        
        linear_part_22 = sum(list_math_multiplication(entry.linear_sum, entry.linear_sum));
        variance_part_third = -( entry.square_sum - (2.0 / entry.number_points) * linear_part_22 + entry.number_points * (1.0 / entry.number_points ** 2.0) * linear_part_22 );

        return (variance_part_first + variance_part_second + variance_part_third);