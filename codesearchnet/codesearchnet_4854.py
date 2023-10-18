def __splitting_criterion(self, clusters, centers):
        """!
        @brief Calculates splitting criterion for input clusters.
        
        @param[in] clusters (list): Clusters for which splitting criterion should be calculated.
        @param[in] centers (list): Centers of the clusters.
        
        @return (double) Returns splitting criterion. High value of splitting cretion means that current structure is much better.
        
        @see __bayesian_information_criterion(clusters, centers)
        @see __minimum_noiseless_description_length(clusters, centers)
        
        """
        
        if self.__criterion == splitting_type.BAYESIAN_INFORMATION_CRITERION:
            return self.__bayesian_information_criterion(clusters, centers)
        
        elif self.__criterion == splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH:
            return self.__minimum_noiseless_description_length(clusters, centers)
        
        else:
            assert 0;