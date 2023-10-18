def __create_queue(self):
        """!
        @brief Create queue of sorted clusters by distance between them, where first cluster has the nearest neighbor. At the first iteration each cluster contains only one point.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        
        @return (list) Create queue of sorted clusters by distance between them.
        
        """
        
        self.__queue = [cure_cluster(self.__pointer_data[index_point], index_point) for index_point in range(len(self.__pointer_data))]
        
        # set closest clusters
        for i in range(0, len(self.__queue)):
            minimal_distance = float('inf')
            closest_index_cluster = -1
            
            for k in range(0, len(self.__queue)):
                if i != k:
                    dist = self.__cluster_distance(self.__queue[i], self.__queue[k])
                    if dist < minimal_distance:
                        minimal_distance = dist
                        closest_index_cluster = k
            
            self.__queue[i].closest = self.__queue[closest_index_cluster]
            self.__queue[i].distance = minimal_distance
        
        # sort clusters
        self.__queue.sort(key = lambda x: x.distance, reverse = False)