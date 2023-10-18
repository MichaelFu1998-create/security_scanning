def __relocate_cluster(self, cluster):
        """!
        @brief Relocate cluster in list in line with distance order.
        
        @param[in] cluster (cure_cluster): Cluster that should be relocated in line with order.
        
        """
        
        self.__queue.remove(cluster)
        self.__insert_cluster(cluster)