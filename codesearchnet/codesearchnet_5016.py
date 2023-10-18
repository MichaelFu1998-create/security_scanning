def process(self, collect_dynamic = False, order = 0.999):
        """!
        @brief Performs simulation of the oscillatory network.
        
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        @param[in] order (double): Order of process synchronization that should be considered as end of clustering, destributed 0..1.
        
        @return (tuple) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see get_som_clusters()
        @see get_clusters()
        """
        
        # train self-organization map.
        self._som.train(self._data, 100);
        
        # prepare to build list.
        weights = list();
        self._som_osc_table.clear();        # must be cleared, if it's used before.
        for i in range(self._som.size):
            if (self._som.awards[i] > 0):
                weights.append(self._som.weights[i]);
                self._som_osc_table.append(i);
        
        # create oscillatory neural network.
        self._sync = self.__create_sync_layer(weights);
        self._analyser = self._sync.process(order, collect_dynamic = collect_dynamic);
        
        return (self._analyser.time, self._analyser.output);