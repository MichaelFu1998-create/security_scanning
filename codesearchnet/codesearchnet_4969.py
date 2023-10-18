def _create_connections(self, conn_type):
        """!
        @brief Create connections in line with input rule (grid four, grid eight, honeycomb, function neighbour).
        
        @param[in] conn_type (type_conn): Type of connection between oscillators in the network.
        
        """
        
        self._neighbors = [[] for index in range(self._size)]
            
        for index in range(0, self._size, 1):
            upper_index = index - self._cols
            upper_left_index = index - self._cols - 1
            upper_right_index = index - self._cols + 1
            
            lower_index = index + self._cols
            lower_left_index = index + self._cols - 1
            lower_right_index = index + self._cols + 1
            
            left_index = index - 1
            right_index = index + 1
            
            node_row_index = math.floor(index / self._cols)
            upper_row_index = node_row_index - 1
            lower_row_index = node_row_index + 1
            
            if (conn_type == type_conn.grid_eight) or (conn_type == type_conn.grid_four):
                if upper_index >= 0:
                    self._neighbors[index].append(upper_index)
                    
                if lower_index < self._size:
                    self._neighbors[index].append(lower_index)
            
            if (conn_type == type_conn.grid_eight) or (conn_type == type_conn.grid_four) or (conn_type == type_conn.honeycomb):
                if (left_index >= 0) and (math.floor(left_index / self._cols) == node_row_index):
                    self._neighbors[index].append(left_index)
                
                if (right_index < self._size) and (math.floor(right_index / self._cols) == node_row_index):
                    self._neighbors[index].append(right_index)
                
                
            if conn_type == type_conn.grid_eight:
                if (upper_left_index >= 0) and (math.floor(upper_left_index / self._cols) == upper_row_index):
                    self._neighbors[index].append(upper_left_index)
                
                if (upper_right_index >= 0) and (math.floor(upper_right_index / self._cols) == upper_row_index):
                    self._neighbors[index].append(upper_right_index)
                    
                if (lower_left_index < self._size) and (math.floor(lower_left_index / self._cols) == lower_row_index):
                    self._neighbors[index].append(lower_left_index)
                    
                if (lower_right_index < self._size) and (math.floor(lower_right_index / self._cols) == lower_row_index):
                    self._neighbors[index].append(lower_right_index)
                
            
            if conn_type == type_conn.honeycomb:
                if (node_row_index % 2) == 0:
                    upper_left_index = index - self._cols
                    upper_right_index = index - self._cols + 1
                
                    lower_left_index = index + self._cols
                    lower_right_index = index + self._cols + 1
                else:
                    upper_left_index = index - self._cols - 1
                    upper_right_index = index - self._cols
                
                    lower_left_index = index + self._cols - 1
                    lower_right_index = index + self._cols
                
                if (upper_left_index >= 0) and (math.floor(upper_left_index / self._cols) == upper_row_index):
                    self._neighbors[index].append(upper_left_index)
                
                if (upper_right_index >= 0) and (math.floor(upper_right_index / self._cols) == upper_row_index):
                    self._neighbors[index].append(upper_right_index)
                    
                if (lower_left_index < self._size) and (math.floor(lower_left_index / self._cols) == lower_row_index):
                    self._neighbors[index].append(lower_left_index)
                    
                if (lower_right_index < self._size) and (math.floor(lower_right_index / self._cols) == lower_row_index):
                    self._neighbors[index].append(lower_right_index)