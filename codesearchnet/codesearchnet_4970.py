def _competition(self, x):
        """!
        @brief Calculates neuron winner (distance, neuron index).
        
        @param[in] x (list): Input pattern from the input data set, for example it can be coordinates of point.
        
        @return (uint) Returns index of neuron that is winner.
        
        """
        
        index = 0
        minimum = euclidean_distance_square(self._weights[0], x)
        
        for i in range(1, self._size, 1):
            candidate = euclidean_distance_square(self._weights[i], x)
            if candidate < minimum:
                index = i
                minimum = candidate
        
        return index