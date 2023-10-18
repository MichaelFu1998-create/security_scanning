def allocate_sync_ensembles(self):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each
               synchronous ensemble corresponds to only one cluster.
        
        @return (list) Grours (lists) of indexes of synchronous oscillators. 
                For example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
                
        """
        
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_allocate_sync_ensembles(self.__ccore_pcnn_dynamic_pointer)
        
        sync_ensembles = []
        traverse_oscillators = set()
        
        number_oscillators = len(self.__dynamic[0])
        
        for t in range(len(self.__dynamic) - 1, 0, -1):
            sync_ensemble = []
            for i in range(number_oscillators):
                if self.__dynamic[t][i] == self.__OUTPUT_TRUE:
                    if i not in traverse_oscillators:
                        sync_ensemble.append(i)
                        traverse_oscillators.add(i)
            
            if sync_ensemble != []:
                sync_ensembles.append(sync_ensemble)
        
        return sync_ensembles