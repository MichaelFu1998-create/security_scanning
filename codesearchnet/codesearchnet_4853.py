def __improve_structure(self, clusters, centers):
        """!
        @brief Check for best structure: divides each cluster into two and checks for best results using splitting criterion.
        
        @param[in] clusters (list): Clusters that have been allocated (each cluster contains indexes of points from data).
        @param[in] centers (list): Centers of clusters.
        
        @return (list) Allocated centers for clustering.
        
        """

        allocated_centers = []
        amount_free_centers = self.__kmax - len(centers)

        for index_cluster in range(len(clusters)):
            # solve k-means problem for children where data of parent are used.
            (parent_child_clusters, parent_child_centers) = self.__improve_parameters(None, clusters[index_cluster])
              
            # If it's possible to split current data
            if len(parent_child_clusters) > 1:
                # Calculate splitting criterion
                parent_scores = self.__splitting_criterion([ clusters[index_cluster] ], [ centers[index_cluster] ])
                child_scores = self.__splitting_criterion([ parent_child_clusters[0], parent_child_clusters[1] ], parent_child_centers)
              
                split_require = False
                
                # Reallocate number of centers (clusters) in line with scores
                if self.__criterion == splitting_type.BAYESIAN_INFORMATION_CRITERION:
                    if parent_scores < child_scores: split_require = True
                    
                elif self.__criterion == splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH:
                    # If its score for the split structure with two children is smaller than that for the parent structure, 
                    # then representing the data samples with two clusters is more accurate in comparison to a single parent cluster.
                    if parent_scores > child_scores: split_require = True;
                
                if (split_require is True) and (amount_free_centers > 0):
                    allocated_centers.append(parent_child_centers[0])
                    allocated_centers.append(parent_child_centers[1])
                    
                    amount_free_centers -= 1
                else:
                    allocated_centers.append(centers[index_cluster])

                    
            else:
                allocated_centers.append(centers[index_cluster])
          
        return allocated_centers