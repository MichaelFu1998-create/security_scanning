def get_neighbors(self, index):
        """!
        @brief Finds neighbors of the oscillator with specified index.
        
        @param[in] index (uint): index of oscillator for which neighbors should be found in the network.
        
        @return (list) Indexes of neighbors of the specified oscillator.
        
        """
        
        if (self._conn_represent == conn_represent.LIST):
            return self._osc_conn[index];      # connections are represented by list.
        elif (self._conn_represent == conn_represent.MATRIX):
            return [neigh_index for neigh_index in range(self._num_osc) if self._osc_conn[index][neigh_index] == True];
        else:
            raise NameError("Unknown type of representation of connections");