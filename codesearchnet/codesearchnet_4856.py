def __bayesian_information_criterion(self, clusters, centers):
        """!
        @brief Calculates splitting criterion for input clusters using bayesian information criterion.
        
        @param[in] clusters (list): Clusters for which splitting criterion should be calculated.
        @param[in] centers (list): Centers of the clusters.
        
        @return (double) Splitting criterion in line with bayesian information criterion.
                High value of splitting criterion means that current structure is much better.
                
        @see __minimum_noiseless_description_length(clusters, centers)
        
        """

        scores = [float('inf')] * len(clusters)     # splitting criterion
        dimension = len(self.__pointer_data[0])
          
        # estimation of the noise variance in the data set
        sigma_sqrt = 0.0
        K = len(clusters)
        N = 0.0
          
        for index_cluster in range(0, len(clusters), 1):
            for index_object in clusters[index_cluster]:
                sigma_sqrt += euclidean_distance_square(self.__pointer_data[index_object], centers[index_cluster]);

            N += len(clusters[index_cluster])
      
        if N - K > 0:
            sigma_sqrt /= (N - K)
            p = (K - 1) + dimension * K + 1

            # in case of the same points, sigma_sqrt can be zero (issue: #407)
            sigma_multiplier = 0.0
            if sigma_sqrt <= 0.0:
                sigma_multiplier = float('-inf')
            else:
                sigma_multiplier = dimension * 0.5 * log(sigma_sqrt)
            
            # splitting criterion    
            for index_cluster in range(0, len(clusters), 1):
                n = len(clusters[index_cluster])

                L = n * log(n) - n * log(N) - n * 0.5 * log(2.0 * numpy.pi) - n * sigma_multiplier - (n - K) * 0.5
                
                # BIC calculation
                scores[index_cluster] = L - p * 0.5 * log(N)
                
        return sum(scores)