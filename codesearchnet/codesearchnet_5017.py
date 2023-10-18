def __create_sync_layer(self, weights):
        """!
        @brief Creates second layer of the network.
        
        @param[in] weights (list): List of weights of SOM neurons.
        
        @return (syncnet) Second layer of the network.
        
        """
        sync_layer = syncnet(weights, 0.0, initial_phases = initial_type.RANDOM_GAUSSIAN, ccore = False);
        
        for oscillator_index1 in range(0, len(sync_layer)):
            for oscillator_index2 in range(oscillator_index1 + 1, len(sync_layer)):
                if (self.__has_object_connection(oscillator_index1, oscillator_index2)):
                    sync_layer.set_connection(oscillator_index1, oscillator_index2);
        
        return sync_layer;