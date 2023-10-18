def __has_object_connection(self, oscillator_index1, oscillator_index2):
        """!
        @brief Searches for pair of objects that are encoded by specified neurons and that are connected in line with connectivity radius.
        
        @param[in] oscillator_index1 (uint): Index of the first oscillator in the second layer.
        @param[in] oscillator_index2 (uint): Index of the second oscillator in the second layer.
        
        @return (bool) True - if there is pair of connected objects encoded by specified oscillators.
        
        """
        som_neuron_index1 = self._som_osc_table[oscillator_index1];
        som_neuron_index2 = self._som_osc_table[oscillator_index2];
        
        for index_object1 in self._som.capture_objects[som_neuron_index1]:
            for index_object2 in self._som.capture_objects[som_neuron_index2]:
                distance = euclidean_distance_square(self._data[index_object1], self._data[index_object2]);
                if (distance <= self._radius):
                    return True;
        
        return False;