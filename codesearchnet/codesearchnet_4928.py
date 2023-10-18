def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Means algorithm.

        @return (kmeans) Returns itself (K-Means instance).

        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_centers()
        
        """

        if len(self.__pointer_data[0]) != len(self.__centers[0]):
            raise ValueError("Dimension of the input data and dimension of the initial cluster centers must be equal.")

        if self.__ccore is True:
            self.__process_by_ccore()
        else:
            self.__process_by_python()

        return self