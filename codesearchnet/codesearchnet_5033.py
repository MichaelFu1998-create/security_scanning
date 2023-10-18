def __cluster_distance(self, cluster1, cluster2):
        """!
        @brief Calculate minimal distance between clusters using representative points.
        
        @param[in] cluster1 (cure_cluster): The first cluster.
        @param[in] cluster2 (cure_cluster): The second cluster.
        
        @return (double) Euclidean distance between two clusters that is defined by minimum distance between representation points of two clusters.
        
        """
        
        distance = float('inf')
        for i in range(0, len(cluster1.rep)):
            for k in range(0, len(cluster2.rep)):
                dist = euclidean_distance_square(cluster1.rep[i], cluster2.rep[k]);   # Fast mode
                #dist = euclidean_distance(cluster1.rep[i], cluster2.rep[k])        # Slow mode
                if dist < distance:
                    distance = dist
                    
        return distance