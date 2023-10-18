def __initialize_locations(self, rows, cols):
        """!
        @brief Initialize locations (coordinates in SOM grid) of each neurons in the map.
        
        @param[in] rows (uint): Number of neurons in the column (number of rows).
        @param[in] cols (uint): Number of neurons in the row (number of columns).
        
        @return (list) List of coordinates of each neuron in map.
        
        """
        
        location = list()
        for i in range(rows):
            for j in range(cols):
                location.append([float(i), float(j)])
        
        return location