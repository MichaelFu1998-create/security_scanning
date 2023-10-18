def notify(self, clusters, centers):
        """!
        @brief This method is called by K-Means algorithm to notify about changes.
        
        @param[in] clusters (array_like): Allocated clusters by K-Means algorithm.
        @param[in] centers (array_like): Allocated centers by K-Means algorithm.
        
        """
        self.__evolution_clusters.append(clusters)
        self.__evolution_centers.append(centers)