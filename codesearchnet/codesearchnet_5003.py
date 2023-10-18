def sync_local_order(self):
        """!
        @brief Calculates current level of local (partial) synchronization in the network.
        
        @return (double) Level of local (partial) synchronization.
        
        @see sync_order()
        
        """
        
        if (self._ccore_network_pointer is not None):
            return wrapper.sync_local_order(self._ccore_network_pointer);
        
        return order_estimator.calculate_local_sync_order(self._phases, self);