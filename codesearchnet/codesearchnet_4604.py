def __create_none_connections(self):
        """!
        @brief Creates network without connections.
        
        """
        if (self._conn_represent == conn_represent.MATRIX):
            for _ in range(0, self._num_osc, 1):
                self._osc_conn.append([False] * self._num_osc);
        elif (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for _ in range(0, self._num_osc, 1)];