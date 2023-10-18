def get_diameter(self):
        """!
        @brief Calculates diameter of cluster that is represented by the entry.
        @details It's calculated once when it's requested after the last changes.
        
        @return (double) Diameter of cluster that is represented by the entry.
        
        """
        
        if (self.__diameter is not None):
            return self.__diameter;
        
        diameter_part = 0.0;
        if (type(self.linear_sum) == list):
            diameter_part = self.square_sum * self.number_points - 2.0 * sum(list_math_multiplication(self.linear_sum, self.linear_sum)) + self.square_sum * self.number_points;
        else:
            diameter_part = self.square_sum * self.number_points - 2.0 * self.linear_sum * self.linear_sum + self.square_sum * self.number_points;
            
        self.__diameter = ( diameter_part / (self.number_points * (self.number_points - 1)) ) ** 0.5;
        return self.__diameter;