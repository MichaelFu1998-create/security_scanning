def __create_grid_eight_connections(self):
        """!
        @brief Creates network with connections that make up eight grid structure.
        @details Each oscillator may be connected with eight neighbors in line with grid structure: right, right-upper, upper, upper-left, left, left-lower, lower, lower-right.
        
        """
        
        self.__create_grid_four_connections();     # create connection with right, upper, left, lower.
        side_size = self.__width;
        
        for index in range(0, self._num_osc, 1):
            upper_left_index = index - side_size - 1;
            upper_right_index = index - side_size + 1;
            
            lower_left_index = index + side_size - 1;
            lower_right_index = index + side_size + 1;
            
            node_row_index = math.floor(index / side_size);
            upper_row_index = node_row_index - 1;
            lower_row_index = node_row_index + 1;
            
            if ( (upper_left_index >= 0) and (math.floor(upper_left_index / side_size) == upper_row_index) ):
                self.__create_connection(index, upper_left_index);
            
            if ( (upper_right_index >= 0) and (math.floor(upper_right_index / side_size) == upper_row_index) ):
                self.__create_connection(index, upper_right_index);
                
            if ( (lower_left_index < self._num_osc) and (math.floor(lower_left_index / side_size) == lower_row_index) ):
                self.__create_connection(index, lower_left_index);
                
            if ( (lower_right_index < self._num_osc) and (math.floor(lower_right_index / side_size) == lower_row_index) ):
                self.__create_connection(index, lower_right_index);