def __create_stimulus(self, stimulus):
        """!
        @brief Create stimulus for oscillators in line with stimulus map and parameters.
        
        @param[in] stimulus (list): Stimulus for oscillators that is represented by list, number of stimulus should be equal number of oscillators.
        
        """
        
        if (len(stimulus) != self._num_osc):
            raise NameError("Number of stimulus should be equal number of oscillators in the network.");
        else:
            self._stimulus = [];
             
            for val in stimulus:
                if (val > 0): self._stimulus.append(self._params.I);
                else: self._stimulus.append(0);