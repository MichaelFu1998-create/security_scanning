def __insert_represented_points(self, cluster):
        """!
        @brief Insert representation points to the k-d tree.
        
        @param[in] cluster (cure_cluster): Cluster whose representation points should be inserted.
        
        """
        
        for point in cluster.rep:
            self.__tree.insert(point, cluster)