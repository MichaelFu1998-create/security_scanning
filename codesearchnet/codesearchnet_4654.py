def __insert_data(self):
        """!
        @brief Inserts input data to the tree.
        
        @remark If number of maximum number of entries is exceeded than diameter is increased and tree is rebuilt.
        
        """
        
        for index_point in range(0, len(self.__pointer_data)):
            point = self.__pointer_data[index_point];
            self.__tree.insert_cluster( [ point ] );
            
            if (self.__tree.amount_entries > self.__entry_size_limit):
                self.__tree = self.__rebuild_tree(index_point);