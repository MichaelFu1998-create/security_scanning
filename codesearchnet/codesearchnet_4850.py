def process(self):
        """!
        @brief Performs cluster analysis in line with rules of X-Means algorithm.
        
        @remark Results of clustering can be obtained using corresponding gets methods.
        
        @see get_clusters()
        @see get_centers()
        
        """
        
        if (self.__ccore is True):
            self.__clusters, self.__centers = wrapper.xmeans(self.__pointer_data, self.__centers, self.__kmax, self.__tolerance, self.__criterion)

        else:
            self.__clusters = []
            while len(self.__centers) <= self.__kmax:
                current_cluster_number = len(self.__centers)
                
                self.__clusters, self.__centers = self.__improve_parameters(self.__centers)
                allocated_centers = self.__improve_structure(self.__clusters, self.__centers)
                
                if current_cluster_number == len(allocated_centers):
                #if ( (current_cluster_number == len(allocated_centers)) or (len(allocated_centers) > self.__kmax) ):
                    break
                else:
                    self.__centers = allocated_centers
            
            self.__clusters, self.__centers = self.__improve_parameters(self.__centers)