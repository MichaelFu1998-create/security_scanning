def calculate_connvectivity_radius(self, amount_clusters, maximum_iterations = 100):
        """!
        @brief Calculates connectivity radius of allocation specified amount of clusters using ordering diagram and marks borders of clusters using indexes of values of ordering diagram.
        @details Parameter 'maximum_iterations' is used to protect from hanging when it is impossible to allocate specified number of clusters.
        
        @param[in] amount_clusters (uint): amount of clusters that should be allocated by calculated connectivity radius.
        @param[in] maximum_iterations (uint): maximum number of iteration for searching connectivity radius to allocated specified amount of clusters (by default it is restricted by 100 iterations).
        
        @return (double, list) Value of connectivity radius and borders of clusters like (radius, borders), radius may be 'None' as well as borders may be '[]'
                                if connectivity radius hasn't been found for the specified amount of iterations.
        
        """
        
        maximum_distance = max(self.__ordering)
        
        upper_distance = maximum_distance
        lower_distance = 0.0

        result = None
        
        amount, borders = self.extract_cluster_amount(maximum_distance)
        if amount <= amount_clusters:
            for _ in range(maximum_iterations):
                radius = (lower_distance + upper_distance) / 2.0
                
                amount, borders = self.extract_cluster_amount(radius)
                if amount == amount_clusters:
                    result = radius
                    break
                
                elif amount == 0:
                    break
                
                elif amount > amount_clusters:
                    lower_distance = radius
                
                elif amount < amount_clusters:
                    upper_distance = radius
        
        return result, borders