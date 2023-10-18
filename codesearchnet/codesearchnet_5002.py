def sync_order(self):
        """!
        @brief Calculates current level of global synchorization (order parameter) in the network.
        @details This parameter is tend 1.0 when the oscillatory network close to global synchronization and it tend to 0.0 when 
                  desynchronization is observed in the network. Order parameter is calculated using following equation:
                  
                  \f[
                  r_{c}=\frac{1}{Ne^{i\varphi }}\sum_{j=0}^{N}e^{i\theta_{j}};
                  \f]
                  
                  where \f$\varphi\f$ is a average phase coordinate in the network, \f$N\f$ is an amount of oscillators in the network.
        
        Example:
        @code
            oscillatory_network = sync(16, type_conn = conn_type.ALL_TO_ALL);
            output_dynamic = oscillatory_network.simulate_static(100, 10);
            
            if (oscillatory_network.sync_order() < 0.9): print("Global synchronization is not reached yet.");
            else: print("Global synchronization is reached.");
        @endcode
        
        @return (double) Level of global synchronization (order parameter).
        
        @see sync_local_order()
        
        """
        
        if (self._ccore_network_pointer is not None):
            return wrapper.sync_order(self._ccore_network_pointer);
        
        return order_estimator.calculate_sync_order(self._phases);