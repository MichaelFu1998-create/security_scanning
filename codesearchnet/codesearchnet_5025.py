def __insert_cluster(self, cluster):
        """!
        @brief Insert cluster to the list (sorted queue) in line with sequence order (distance).
        
        @param[in] cluster (cure_cluster): Cluster that should be inserted.
        
        """
        
        for index in range(len(self.__queue)):
            if cluster.distance < self.__queue[index].distance:
                self.__queue.insert(index, cluster)
                return
    
        self.__queue.append(cluster)