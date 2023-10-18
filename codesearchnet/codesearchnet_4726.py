def process(self):
        """!
        @brief Performs cluster analysis in line with rules of DBSCAN algorithm.
        
        @see get_clusters()
        @see get_noise()
        
        """
        
        if self.__ccore is True:
            (self.__clusters, self.__noise) = wrapper.dbscan(self.__pointer_data, self.__eps, self.__neighbors, self.__data_type)
            
        else:
            if self.__data_type == 'points':
                self.__kdtree = kdtree(self.__pointer_data, range(len(self.__pointer_data)))

            for i in range(0, len(self.__pointer_data)):
                if self.__visited[i] is False:
                    cluster = self.__expand_cluster(i)
                    if cluster is not None:
                        self.__clusters.append(cluster)

            for i in range(0, len(self.__pointer_data)):
                if self.__belong[i] is False:
                    self.__noise.append(i)