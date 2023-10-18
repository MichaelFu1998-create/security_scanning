def __minimum_noiseless_description_length(self, clusters, centers):
        """!
        @brief Calculates splitting criterion for input clusters using minimum noiseless description length criterion.
        
        @param[in] clusters (list): Clusters for which splitting criterion should be calculated.
        @param[in] centers (list): Centers of the clusters.
        
        @return (double) Returns splitting criterion in line with bayesian information criterion. 
                Low value of splitting cretion means that current structure is much better.
        
        @see __bayesian_information_criterion(clusters, centers)
        
        """
        
        scores = float('inf')
        
        W = 0.0
        K = len(clusters)
        N = 0.0

        sigma_sqrt = 0.0
        
        alpha = 0.9
        betta = 0.9
        
        for index_cluster in range(0, len(clusters), 1):
            Ni = len(clusters[index_cluster])
            if Ni == 0:
                return float('inf')
            
            Wi = 0.0
            for index_object in clusters[index_cluster]:
                # euclidean_distance_square should be used in line with paper, but in this case results are
                # very poor, therefore square root is used to improved.
                Wi += euclidean_distance(self.__pointer_data[index_object], centers[index_cluster])
            
            sigma_sqrt += Wi
            W += Wi / Ni
            N += Ni
        
        if N - K > 0:
            sigma_sqrt /= (N - K)
            sigma = sigma_sqrt ** 0.5
            
            Kw = (1.0 - K / N) * sigma_sqrt
            Ks = ( 2.0 * alpha * sigma / (N ** 0.5) ) * ( (alpha ** 2.0) * sigma_sqrt / N + W - Kw / 2.0 ) ** 0.5
            
            scores = sigma_sqrt * (2 * K)**0.5 * ((2 * K)**0.5 + betta) / N + W - sigma_sqrt + Ks + 2 * alpha**0.5 * sigma_sqrt / N
        
        return scores