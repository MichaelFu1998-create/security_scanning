def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = True):
        """!
        @brief Peforms cluster analysis using simulation of the oscillatory network.
        
        @param[in] order (double): Order of synchronization that is used as indication for stopping processing.
        @param[in] solution (solve_type): Specified type of solving diff. equation.
        @param[in] collect_dynamic (bool): Specified requirement to collect whole dynamic of the network.
        
        @return (syncnet_analyser) Returns analyser of results of clustering.
        
        """
        
        if (self._ccore_network_pointer is not None):
            pointer_output_dynamic = syncnet_process(self._ccore_network_pointer, order, solution, collect_dynamic);
            return syncnet_analyser(None, None, pointer_output_dynamic);
        else:
            output_sync_dynamic = self.simulate_dynamic(order, solution, collect_dynamic);
            return syncnet_analyser(output_sync_dynamic.output, output_sync_dynamic.time, None);