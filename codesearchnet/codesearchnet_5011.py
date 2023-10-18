def has_connection(self, i, j):
        """!
        @brief Returns True if there is connection between i and j oscillators and False - if connection doesn't exist.
        
        @param[in] i (uint): index of an oscillator in the network.
        @param[in] j (uint): index of an oscillator in the network.
        
        """
        
        if ( (self._ccore_network_pointer is not None) and (self._osc_conn is None) ):
            self._osc_conn = wrapper.sync_connectivity_matrix(self._ccore_network_pointer);
        
        return super().has_connection(i, j);