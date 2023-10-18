def has_connection(self, i, j):
        """!
        @brief Returns True if there is connection between i and j oscillators and False - if connection doesn't exist.
        
        @param[in] i (uint): index of an oscillator in the network.
        @param[in] j (uint): index of an oscillator in the network.
        
        """
        if (self._conn_represent == conn_represent.MATRIX):
            return (self._osc_conn[i][j]);
        
        elif (self._conn_represent == conn_represent.LIST):
            for neigh_index in range(0, len(self._osc_conn[i]), 1):
                if (self._osc_conn[i][neigh_index] == j):
                    return True;
            return False;
        
        else:
            raise NameError("Unknown type of representation of coupling");