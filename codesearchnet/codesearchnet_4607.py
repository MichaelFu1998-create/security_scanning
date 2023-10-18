def set_connection(self, i, j):
        """!
        @brief Couples two specified oscillators in the network with dynamic connections.
        
        @param[in] i (uint): index of an oscillator that should be coupled with oscillator 'j' in the network.
        @param[in] j (uint): index of an oscillator that should be coupled with oscillator 'i' in the network.
        
        @note This method can be used only in case of DYNAMIC connections, otherwise it throws expection.
        
        """
        
        if (self.structure != conn_type.DYNAMIC):
            raise NameError("Connection between oscillators can be changed only in case of dynamic type.");
        
        if (self._conn_represent == conn_represent.MATRIX):
            self._osc_conn[i][j] = True;
            self._osc_conn[j][i] = True;
        else:
            self._osc_conn[i].append(j);
            self._osc_conn[j].append(i);