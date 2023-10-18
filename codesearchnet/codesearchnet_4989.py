def calculate_order_parameter(self, start_iteration = None, stop_iteration = None):
        """!
        @brief Calculates level of global synchorization (order parameter).
        @details This parameter is tend 1.0 when the oscillatory network close to global synchronization and it tend to 0.0 when 
                  desynchronization is observed in the network. Order parameter is calculated using following equation:
                  
                  \f[
                  r_{c}=\frac{1}{Ne^{i\varphi }}\sum_{j=0}^{N}e^{i\theta_{j}};
                  \f]
                  
                  where \f$\varphi\f$ is a average phase coordinate in the network, \f$N\f$ is an amount of oscillators in the network.
        
        @param[in] start_iteration (uint): The first iteration that is used for calculation, if 'None' then the last iteration is used.
        @param[in] stop_iteration (uint): The last iteration that is used for calculation, if 'None' then 'start_iteration' + 1 is used.
        
        Example:
        @code
            oscillatory_network = sync(16, type_conn = conn_type.ALL_TO_ALL);
            output_dynamic = oscillatory_network.simulate_static(100, 10);
            
            print("Order parameter at the last step: ", output_dynamic.calculate_order_parameter());
            print("Order parameter at the first step:", output_dynamic.calculate_order_parameter(0));
            print("Order parameter evolution between 40 and 50 steps:", output_dynamic.calculate_order_parameter(40, 50));
        @endcode
        
        @return (list) List of levels of global synchronization (order parameter evolution).
        
        @see order_estimator
        
        """
        
        (start_iteration, stop_iteration) = self.__get_start_stop_iterations(start_iteration, stop_iteration);
        
        if (self._ccore_sync_dynamic_pointer is not None):
            return wrapper.sync_dynamic_calculate_order(self._ccore_sync_dynamic_pointer, start_iteration, stop_iteration);
        
        sequence_order = [];
        for index in range(start_iteration, stop_iteration):
            sequence_order.append(order_estimator.calculate_sync_order(self.output[index]));
        
        return sequence_order;