def __delete_represented_points(self, cluster): 
        """!
        @brief Remove representation points of clusters from the k-d tree
        
        @param[in] cluster (cure_cluster): Cluster whose representation points should be removed.
        
        """
        
        for point in cluster.rep:
            self.__tree.remove(point, payload=cluster)