def get_radius(self):
        """!
        @brief Calculates radius of cluster that is represented by the entry.
        @details It's calculated once when it's requested after the last changes.
        
        @return (double) Radius of cluster that is represented by the entry.
        
        """
        
        if (self.__radius is not None):
            return self.__radius;
        
        centroid = self.get_centroid();
        
        radius_part_1 = self.square_sum;
        
        radius_part_2 = 0.0;
        radius_part_3 = 0.0;
        
        if (type(centroid) == list):
            radius_part_2 = 2.0 * sum(list_math_multiplication(self.linear_sum, centroid));
            radius_part_3 = self.number_points * sum(list_math_multiplication(centroid, centroid));
        else:
            radius_part_2 = 2.0 * self.linear_sum * centroid;
            radius_part_3 = self.number_points * centroid * centroid;
        
        self.__radius = ( (1.0 / self.number_points) * (radius_part_1 - radius_part_2 + radius_part_3) ) ** 0.5;
        return self.__radius;