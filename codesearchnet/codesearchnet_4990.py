def calculate_local_order_parameter(self, oscillatory_network, start_iteration = None, stop_iteration = None):
        """!
        @brief Calculates local order parameter.
        @details Local order parameter or so-called level of local or partial synchronization is calculated by following expression:
        
        \f[
        r_{c}=\left | \sum_{i=0}^{N} \frac{1}{N_{i}} \sum_{j=0}e^{ \theta_{j} - \theta_{i} } \right |;
        \f]
        
        where N - total amount of oscillators in the network and \f$N_{i}\f$ - amount of neighbors of oscillator with index \f$i\f$.
        
        @param[in] oscillatory_network (sync): Sync oscillatory network whose structure of connections is required for calculation.
        @param[in] start_iteration (uint): The first iteration that is used for calculation, if 'None' then the last iteration is used.
        @param[in] stop_iteration (uint): The last iteration that is used for calculation, if 'None' then 'start_iteration' + 1 is used.
        
        @return (list) List of levels of local (partial) synchronization (local order parameter evolution).
        
        """

        (start_iteration, stop_iteration) = self.__get_start_stop_iterations(start_iteration, stop_iteration);
        
        if (self._ccore_sync_dynamic_pointer is not None):
            network_pointer = oscillatory_network._ccore_network_pointer;
            return wrapper.sync_dynamic_calculate_local_order(self._ccore_sync_dynamic_pointer, network_pointer, start_iteration, stop_iteration);
        
        sequence_local_order = [];
        for index in range(start_iteration, stop_iteration):
            sequence_local_order.append(order_estimator.calculate_local_sync_order(self.output[index], oscillatory_network));
        
        return sequence_local_order;