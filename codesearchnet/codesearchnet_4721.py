def process(self):
        """!
        @brief Performs cluster analysis by competition between neurons of SOM.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        
        """
        
        self.__network = som(1, self.__amount_clusters, type_conn.grid_four, None, self.__ccore);
        self.__network.train(self.__data_pointer, self.__epouch, True);