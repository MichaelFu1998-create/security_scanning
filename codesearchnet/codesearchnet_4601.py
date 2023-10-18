def __create_grid_four_connections(self):
        """!
        @brief Creates network with connections that make up four grid structure.
        @details Each oscillator may be connected with four neighbors in line with 'grid' structure: right, upper, left, lower.
        
        """
        
        side_size = self.__width;
        if (self._conn_represent == conn_represent.MATRIX):
            self._osc_conn = [[0] * self._num_osc for index in range(0, self._num_osc, 1)];
        elif (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for index in range(0, self._num_osc, 1)];
        else:
            raise NameError("Unknown type of representation of connections");
        
        for index in range(0, self._num_osc, 1):
            upper_index = index - side_size;
            lower_index = index + side_size;
            left_index = index - 1;
            right_index = index + 1;
            
            node_row_index = math.ceil(index / side_size);
            if (upper_index >= 0):
                self.__create_connection(index, upper_index);
            
            if (lower_index < self._num_osc):
                self.__create_connection(index, lower_index);
            
            if ( (left_index >= 0) and (math.ceil(left_index / side_size) == node_row_index) ):
                self.__create_connection(index, left_index);
            
            if ( (right_index < self._num_osc) and (math.ceil(right_index / side_size) == node_row_index) ):
                self.__create_connection(index, right_index);