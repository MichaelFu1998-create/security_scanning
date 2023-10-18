def get_neighbors(self, index):
        """!
        @brief Finds neighbors of the oscillator with specified index.
        
        @param[in] index (uint): index of oscillator for which neighbors should be found in the network.
        
        @return (list) Indexes of neighbors of the specified oscillator.
        
        """
        
        if ( (self._ccore_network_pointer is not None) and (self._osc_conn is None) ):
            self._osc_conn = wrapper.sync_connectivity_matrix(self._ccore_network_pointer);
            
        return super().get_neighbors(index);