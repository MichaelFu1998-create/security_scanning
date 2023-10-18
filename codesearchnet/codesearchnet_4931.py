def get_centers(self):
        """!
        @brief Returns list of centers of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        if isinstance(self.__centers, list):
            return self.__centers
        
        return self.__centers.tolist()