def __create_all_to_all_connections(self):
        """!
        @brief Creates connections between all oscillators.
        
        """
        
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([True] * self._num_osc);
                self._osc_conn[index][index] = False;
        
        elif (self._conn_represent == conn_represent.LIST):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([neigh for neigh in range(0, self._num_osc, 1) if index != neigh]);