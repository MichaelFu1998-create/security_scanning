def __extract_clusters(self):
        """!
        @brief Extract clusters and noise from order database.
        
        """
     
        self.__clusters = []
        self.__noise = []

        current_cluster = self.__noise
        for optics_object in self.__ordered_database:
            if (optics_object.reachability_distance is None) or (optics_object.reachability_distance > self.__eps):
                if (optics_object.core_distance is not None) and (optics_object.core_distance <= self.__eps):
                    self.__clusters.append([ optics_object.index_object ])
                    current_cluster = self.__clusters[-1]
                else:
                    self.__noise.append(optics_object.index_object)
            else:
                current_cluster.append(optics_object.index_object)