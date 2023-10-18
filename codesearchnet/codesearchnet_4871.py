def __get_neighbors(self, node_index):
        """!
        @brief Returns indexes of neighbors of the specified node.
        
        @param[in] node_index (uint):
        
        @return (list) Neighbors of the specified node.
        
        """
        
        return [ index for index in range(len(self.__data_pointer[node_index])) if self.__data_pointer[node_index][index] != 0 ];