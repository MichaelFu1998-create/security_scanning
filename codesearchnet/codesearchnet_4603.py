def __create_list_bidir_connections(self):
        """!
        @brief Creates network as bidirectional list.
        @details Each oscillator may be conneted with two neighbors in line with classical list structure: right, left.
        
        """
        
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([0] * self._num_osc);
                self._osc_conn[index][index] = False;
                if (index > 0):
                    self._osc_conn[index][index - 1] = True;
                    
                if (index < (self._num_osc - 1)):
                    self._osc_conn[index][index + 1] = True;
        
        elif (self._conn_represent == conn_represent.LIST):
            for index in range(self._num_osc):
                self._osc_conn.append([]);
                if (index > 0):
                    self._osc_conn[index].append(index - 1);
                
                if (index < (self._num_osc - 1)):
                    self._osc_conn[index].append(index + 1);