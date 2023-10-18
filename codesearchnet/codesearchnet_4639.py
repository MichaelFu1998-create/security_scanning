def extract_cluster_amount(self, radius):
        """!
        @brief Obtains amount of clustering that can be allocated by using specified radius for ordering diagram and borders between them.
        @details When growth of reachability-distances is detected than it is considered as a start point of cluster, 
                 than pick is detected and after that recession is observed until new growth (that means end of the
                 current cluster and start of a new one) or end of diagram.
        
        @param[in] radius (double): connectivity radius that is used for cluster allocation.
        
        @return (unit, list) Amount of clusters that can be allocated by the connectivity radius on ordering diagram and borders between them using indexes
                 from ordering diagram (amount_clusters, border_clusters).
        
        """
        
        amount_clusters = 1
        
        cluster_start = False
        cluster_pick = False
        total_similarity = True
        previous_cluster_distance = None
        previous_distance = None
        
        cluster_borders = []
        
        for index_ordering in range(len(self.__ordering)):
            distance = self.__ordering[index_ordering]
            if distance >= radius:
                if cluster_start is False:
                    cluster_start = True
                    amount_clusters += 1
                    
                    if index_ordering != 0:
                        cluster_borders.append(index_ordering)
                
                else:
                    if (distance < previous_cluster_distance) and (cluster_pick is False):
                        cluster_pick = True
                    
                    elif (distance > previous_cluster_distance) and (cluster_pick is True):
                        cluster_pick = False
                        amount_clusters += 1
                        
                        if index_ordering != 0:
                            cluster_borders.append(index_ordering)
                
                previous_cluster_distance = distance
            
            else:
                cluster_start = False
                cluster_pick = False
            
            if (previous_distance is not None) and (distance != previous_distance):
                total_similarity = False
            
            previous_distance = distance
        
        if (total_similarity is True) and (previous_distance > radius):
            amount_clusters = 0

        return amount_clusters, cluster_borders