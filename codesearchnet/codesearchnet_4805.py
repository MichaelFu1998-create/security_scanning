def outputs(self, values):
        """!
        @brief Sets outputs of neurons.
        
        """
        
        self._outputs = [val for val in values];
        self._outputs_buffer = [val for val in values];