def _create_structure(self, type_conn = conn_type.ALL_TO_ALL):
        """!
        @brief Creates connection in line with representation of matrix connections [NunOsc x NumOsc].
        
        @param[in] type_conn (conn_type): Connection type (all-to-all, bidirectional list, grid structure, etc.) that is used by the network.
        
        """
        
        self._osc_conn = list();
        
        if (type_conn == conn_type.NONE):
            self.__create_none_connections();
        
        elif (type_conn == conn_type.ALL_TO_ALL):
            self.__create_all_to_all_connections();
        
        elif (type_conn == conn_type.GRID_FOUR):
            self.__create_grid_four_connections();
            
        elif (type_conn == conn_type.GRID_EIGHT):
            self.__create_grid_eight_connections();
            
        elif (type_conn == conn_type.LIST_BIDIR):
            self.__create_list_bidir_connections();
        
        elif (type_conn == conn_type.DYNAMIC):
            self.__create_dynamic_connection();
        
        else:
            raise NameError('The unknown type of connections');