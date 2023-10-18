def __create_kdtree(self):
        """!
        @brief Create k-d tree in line with created clusters. At the first iteration contains all points from the input data set.
        
        @return (kdtree) k-d tree that consist of representative points of CURE clusters.
        
        """
        
        self.__tree = kdtree()
        for current_cluster in self.__queue:
            for representative_point in current_cluster.rep:
                self.__tree.insert(representative_point, current_cluster)