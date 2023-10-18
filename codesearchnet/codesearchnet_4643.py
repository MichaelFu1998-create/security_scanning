def __allocate_clusters(self):
        """!
        @brief Performs cluster allocation and builds ordering diagram that is based on reachability-distances.
        
        """
        
        self.__initialize(self.__sample_pointer)
        
        for optic_object in self.__optics_objects:
            if optic_object.processed is False:
                self.__expand_cluster_order(optic_object)
        
        self.__extract_clusters()