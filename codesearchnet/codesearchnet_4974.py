def _get_maximal_adaptation(self, previous_weights):
        """!
        @brief Calculates maximum changes of weight in line with comparison between previous weights and current weights.
        
        @param[in] previous_weights (list): Weights from the previous step of learning process.
        
        @return (double) Value that represents maximum changes of weight after adaptation process.
        
        """
        
        dimension = len(self._data[0])
        maximal_adaptation = 0.0
        
        for neuron_index in range(self._size):
            for dim in range(dimension):
                current_adaptation = previous_weights[neuron_index][dim] - self._weights[neuron_index][dim]
                        
                if current_adaptation < 0:
                    current_adaptation = -current_adaptation
                        
                if maximal_adaptation < current_adaptation:
                    maximal_adaptation = current_adaptation
                    
        return maximal_adaptation