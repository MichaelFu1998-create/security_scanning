def train(self, samples):
        """!
        @brief Trains syncpr network using Hebbian rule for adjusting strength of connections between oscillators during training.
        
        @param[in] samples (list): list of patterns where each pattern is represented by list of features that are equal to [-1; 1].
        
        """
        
        # Verify pattern for learning
        for pattern in samples:
            self.__validate_pattern(pattern);
        
        if (self._ccore_network_pointer is not None):
            return wrapper.syncpr_train(self._ccore_network_pointer, samples);
        
        length = len(self);
        number_samples = len(samples);
        
        for i in range(length):
            for j in range(i + 1, len(self), 1):
                
                # go through via all patterns
                for p in range(number_samples):
                    value1 = samples[p][i];
                    value2 = samples[p][j];
                    
                    self._coupling[i][j] += value1 * value2;
                
                self._coupling[i][j] /= length;
                self._coupling[j][i] = self._coupling[i][j];