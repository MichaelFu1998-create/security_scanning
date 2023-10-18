def __find_another_nearest_medoid(self, point_index, current_medoid_index):
        """!
        @brief Finds the another nearest medoid for the specified point that is differ from the specified medoid. 
        
        @param[in] point_index: index of point in dataspace for that searching of medoid in current list of medoids is perfomed.
        @param[in] current_medoid_index: index of medoid that shouldn't be considered as a nearest.
        
        @return (uint) index of the another nearest medoid for the point.
        
        """
        other_medoid_index = -1
        other_distance_nearest = float('inf')
        for index_medoid in self.__current:
            if (index_medoid != current_medoid_index):
                other_distance_candidate = euclidean_distance_square(self.__pointer_data[point_index], self.__pointer_data[current_medoid_index])
                
                if other_distance_candidate < other_distance_nearest:
                    other_distance_nearest = other_distance_candidate
                    other_medoid_index = index_medoid
        
        return other_medoid_index