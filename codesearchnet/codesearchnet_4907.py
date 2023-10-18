def process(self):
        """!
        @brief Performs cluster analysis in line with rules of ROCK algorithm.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        
        """
        
        # TODO: (Not related to specification, just idea) First iteration should be investigated. Euclidean distance should be used for clustering between two 
        # points and rock algorithm between clusters because we consider non-categorical samples. But it is required more investigations.
        
        if (self.__ccore is True):
            self.__clusters = wrapper.rock(self.__pointer_data, self.__eps, self.__number_clusters, self.__threshold);
        
        else:  
            self.__clusters = [[index] for index in range(len(self.__pointer_data))];
            
            while (len(self.__clusters) > self.__number_clusters):
                indexes = self.__find_pair_clusters(self.__clusters);
                
                if (indexes != [-1, -1]):
                    self.__clusters[indexes[0]] += self.__clusters[indexes[1]];
                    self.__clusters.pop(indexes[1]);   # remove merged cluster.
                else:
                    break;