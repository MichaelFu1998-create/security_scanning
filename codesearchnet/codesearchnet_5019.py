def get_som_clusters(self):
        """!
        @brief Returns clusters with SOM neurons that encode input features in line with result of synchronization in the second (Sync) layer.
        
        @return (list) List of clusters that are represented by lists of indexes of neurons that encode input data.
        
        @see process()
        @see get_clusters()
        
        """
        
        sync_clusters = self._analyser.allocate_clusters();
        
        # Decode it to indexes of SOM neurons
        som_clusters = list();
        for oscillators in sync_clusters:
            cluster = list();
            for index_oscillator in oscillators:
                index_neuron = self._som_osc_table[index_oscillator];
                cluster.append(index_neuron);
                
            som_clusters.append(cluster);
            
        return som_clusters;