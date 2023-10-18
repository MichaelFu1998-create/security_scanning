def allocate_spike_ensembles(self):
        """!
        @brief Analyses output dynamic of network and allocates spikes on each iteration as a list of indexes of oscillators.
        @details Each allocated spike ensemble represents list of indexes of oscillators whose output is active.
        
        @return (list) Spike ensembles of oscillators.
        
        """
        
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_allocate_spike_ensembles(self.__ccore_pcnn_dynamic_pointer)
        
        spike_ensembles = []
        number_oscillators = len(self.__dynamic[0])
        
        for t in range(len(self.__dynamic)):
            spike_ensemble = []
            
            for index in range(number_oscillators):
                if self.__dynamic[t][index] == self.__OUTPUT_TRUE:
                    spike_ensemble.append(index)
            
            if len(spike_ensemble) > 0:
                spike_ensembles.append(spike_ensemble)
        
        return spike_ensembles