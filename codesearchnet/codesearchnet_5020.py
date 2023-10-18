def get_clusters(self, eps = 0.1):
        """!
        @brief Returns clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
        
        @param[in] eps (double): Maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) List of grours (lists) of indexes of synchronous oscillators that corresponds to index of objects.
        
        @see process()
        @see get_som_clusters()
        
        """
        
        sync_clusters = self._analyser.allocate_clusters(eps)       # it isn't indexes of SOM neurons
        
        clusters = list()
        for oscillators in sync_clusters:
            cluster = list()
            for index_oscillator in oscillators:
                index_neuron = self._som_osc_table[index_oscillator]
                
                cluster += self._som.capture_objects[index_neuron]
                
            clusters.append(cluster)
        
        return clusters