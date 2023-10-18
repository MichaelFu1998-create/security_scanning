def allocate_sync_ensembles(self, tolerance = 0.1, threshold_steps = 1):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each
               synchronous ensemble corresponds to only one cluster.
               
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        @param[in] threshold_steps (uint): Number of steps from the end of simulation that should be analysed for ensemble allocation.
                    If amout of simulation steps has been less than threshold steps than amount of steps will be reduced to amout
                    of simulation steps.
        
        @return (list) Grours of indexes of synchronous oscillators, for example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ]."
        
        """
        
        clusters = [ [0] ];
        
        number_oscillators = len(self._dynamic[0]);
        
        for i in range(1, number_oscillators, 1):
            captured_neuron = True;
            for cluster in clusters:
                neuron_index = cluster[0];
                
                analysis_steps = threshold_steps;
                if (len(self._dynamic) < analysis_steps):
                    analysis_steps = len(self._dynamic);
                
                analysis_start_step_index = len(self._dynamic) - 1;
                
                for step in range(analysis_start_step_index, analysis_start_step_index - analysis_steps, -1):
                    neuron_amplitude = self._dynamic[step][neuron_index];
                    candidate_amplitude = self._dynamic[step][i];
                    
                    if ( not (candidate_amplitude < (neuron_amplitude + tolerance)) or not (candidate_amplitude > (neuron_amplitude - tolerance)) ):
                        captured_neuron = False;
                        break;
                    
                if ( captured_neuron is True ):
                    cluster.append(i);
                    break;
            
            if (captured_neuron is False):
                clusters.append([i]);
        
        return clusters;