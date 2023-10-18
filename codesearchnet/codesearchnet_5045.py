def __calculate_weight(self, stimulus1, stimulus2):
        """!
        @brief Calculate weight between neurons that have external stimulus1 and stimulus2.
        
        @param[in] stimulus1 (list): External stimulus of the first neuron.
        @param[in] stimulus2 (list): External stimulus of the second neuron.
        
        @return (double) Weight between neurons that are under specified stimulus.
        
        """
        
        distance = euclidean_distance_square(stimulus1, stimulus2)
        return math.exp(-distance / (2.0 * self.__average_distance))