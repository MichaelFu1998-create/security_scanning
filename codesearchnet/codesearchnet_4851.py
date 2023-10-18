def __improve_parameters(self, centers, available_indexes = None):
        """!
        @brief Performs k-means clustering in the specified region.
        
        @param[in] centers (list): Centers of clusters.
        @param[in] available_indexes (list): Indexes that defines which points can be used for k-means clustering, if None - then all points are used.
        
        @return (list) List of allocated clusters, each cluster contains indexes of objects in list of data.
        
        """

        if available_indexes and len(available_indexes) == 1:
            index_center = available_indexes[0]
            return [ available_indexes ], self.__pointer_data[index_center]

        local_data = self.__pointer_data
        if available_indexes:
            local_data = [ self.__pointer_data[i] for i in available_indexes ]

        local_centers = centers
        if centers is None:
            local_centers = kmeans_plusplus_initializer(local_data, 2, kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE).initialize()

        kmeans_instance = kmeans(local_data, local_centers, tolerance=self.__tolerance, ccore=False)
        kmeans_instance.process()

        local_centers = kmeans_instance.get_centers()
        
        clusters = kmeans_instance.get_clusters()
        if available_indexes:
            clusters = self.__local_to_global_clusters(clusters, available_indexes)
        
        return clusters, local_centers