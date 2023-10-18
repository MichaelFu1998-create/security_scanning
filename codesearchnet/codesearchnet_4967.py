def __initialize_distances(self, size, location):
        """!
        @brief Initialize distance matrix in SOM grid.
        
        @param[in] size (uint): Amount of neurons in the network.
        @param[in] location (list): List of coordinates of each neuron in the network.
        
        @return (list) Distance matrix between neurons in the network.
        
        """
        sqrt_distances = [ [ [] for i in range(size) ] for j in range(size) ]
        for i in range(size):
            for j in range(i, size, 1):
                dist = euclidean_distance_square(location[i], location[j])
                sqrt_distances[i][j] = dist
                sqrt_distances[j][i] = dist
        
        return sqrt_distances