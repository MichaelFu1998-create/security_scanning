def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs clustering of input data set in line with input parameters.
        
        @param[in] order (double): Level of local synchronization between oscillator that defines end of synchronization process, range [0..1].
        @param[in] solution (solve_type) Type of solving differential equation.
        @param[in] collect_dynamic (bool): If True - returns whole history of process synchronization otherwise - only final state (when process of clustering is over).
        
        @return (tuple) Returns dynamic of the network as tuple of lists on each iteration (time, oscillator_phases) that depends on collect_dynamic parameter. 
        
        @see get_clusters()
        
        """
        
        if (self.__ccore_network_pointer is not None):
            analyser = wrapper.hsyncnet_process(self.__ccore_network_pointer, order, solution, collect_dynamic);
            return syncnet_analyser(None, None, analyser);
        
        number_neighbors = self.__initial_neighbors;
        current_number_clusters = float('inf');
        
        dyn_phase = [];
        dyn_time = [];
        
        radius = average_neighbor_distance(self._osc_loc, number_neighbors);
        
        increase_step = int(len(self._osc_loc) * self.__increase_persent);
        if (increase_step < 1):
            increase_step = 1;
        
        
        analyser = None;
        while(current_number_clusters > self._number_clusters):
            self._create_connections(radius);
        
            analyser = self.simulate_dynamic(order, solution, collect_dynamic);
            if (collect_dynamic == True):
                if (len(dyn_phase) == 0):
                    self.__store_dynamic(dyn_phase, dyn_time, analyser, True);
                
                self.__store_dynamic(dyn_phase, dyn_time, analyser, False);
            
            clusters = analyser.allocate_sync_ensembles(0.05);
            
            # Get current number of allocated clusters
            current_number_clusters = len(clusters);
            
            # Increase number of neighbors that should be used
            number_neighbors += increase_step;
            
            # Update connectivity radius and check if average function can be used anymore
            radius = self.__calculate_radius(number_neighbors, radius);
        
        if (collect_dynamic != True):
            self.__store_dynamic(dyn_phase, dyn_time, analyser, False);
        
        return syncnet_analyser(dyn_phase, dyn_time, None);