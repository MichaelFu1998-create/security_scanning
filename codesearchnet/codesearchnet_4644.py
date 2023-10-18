def get_ordering(self):
        """!
        @brief Returns clustering ordering information about the input data set.
        @details Clustering ordering of data-set contains the information about the internal clustering structure in line with connectivity radius.
        
        @return (ordering_analyser) Analyser of clustering ordering.
        
        @see process()
        @see get_clusters()
        @see get_noise()
        @see get_radius()
        @see get_optics_objects()
        
        """
        
        if self.__ordering is None:
            self.__ordering = []
        
            for cluster in self.__clusters:
                for index_object in cluster:
                    optics_object = self.__optics_objects[index_object]
                    if optics_object.reachability_distance is not None:
                        self.__ordering.append(optics_object.reachability_distance)
            
        return self.__ordering