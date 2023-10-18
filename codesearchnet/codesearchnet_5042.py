def __create_weights(self, stimulus):
        """!
        @brief Create weights between neurons in line with stimulus.
        
        @param[in] stimulus (list): External stimulus for the chaotic neural network.
        
        """
        
        self.__average_distance = average_neighbor_distance(stimulus, self.__amount_neighbors)
        
        self.__weights = [ [ 0.0 for _ in range(len(stimulus)) ] for _ in range(len(stimulus)) ]
        self.__weights_summary = [ 0.0 for _ in range(self.__num_osc) ]
        
        if self.__conn_type == type_conn.ALL_TO_ALL:
            self.__create_weights_all_to_all(stimulus)
        
        elif self.__conn_type == type_conn.TRIANGULATION_DELAUNAY:
            self.__create_weights_delaunay_triangulation(stimulus)