def allocate_sync_ensembles(dynamic, tolerance = 0.1, threshold = 1.0, ignore = None):
    """!
    @brief Allocate clusters in line with ensembles of synchronous oscillators where each
           synchronous ensemble corresponds to only one cluster.
    
    @param[in] dynamic (dynamic): Dynamic of each oscillator.
    @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
    @param[in] threshold (double): Amlitude trigger when spike is taken into account.
    @param[in] ignore (bool): Set of indexes that shouldn't be taken into account.
    
    @return (list) Grours (lists) of indexes of synchronous oscillators, for example, 
            [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
            
    """
    
    descriptors = [ [] for _ in range(len(dynamic[0])) ];
    
    # Check from the end for obtaining result
    for index_dyn in range(0, len(dynamic[0]), 1):
        if ((ignore is not None) and (index_dyn in ignore)):
            continue;
        
        time_stop_simulation = len(dynamic) - 1;
        active_state = False;
        
        if (dynamic[time_stop_simulation][index_dyn] > threshold):
            active_state = True;
            
        # if active state is detected, it means we don't have whole oscillatory period for the considered oscillator, should be skipped.
        if (active_state is True):
            while ( (dynamic[time_stop_simulation][index_dyn] > threshold) and (time_stop_simulation > 0) ):
                time_stop_simulation -= 1;
            
            # if there are no any oscillation than let's consider it like noise
            if (time_stop_simulation == 0):
                continue;
            
            # reset
            active_state = False;
        
        desc = [0, 0, 0]; # end, start, average time of oscillation
        for t in range(time_stop_simulation, 0, -1):
            if ( (dynamic[t][index_dyn] > threshold) and (active_state is False) ):
                desc[0] = t;
                active_state = True;
            elif ( (dynamic[t][index_dyn] < threshold) and (active_state is True) ):
                desc[1] = t;
                active_state = False;
                
                break;
        
        if (desc == [0, 0, 0]):
            continue;
        
        desc[2] = desc[1] + (desc[0] - desc[1]) / 2.0;
        descriptors[index_dyn] = desc;
    
    
    # Cluster allocation
    sync_ensembles = [];
    desc_sync_ensembles = [];
    
    for index_desc in range(0, len(descriptors), 1):
        if (descriptors[index_desc] == []):
            continue;
        
        if (len(sync_ensembles) == 0):
            desc_ensemble = descriptors[index_desc];
            reducer = (desc_ensemble[0] - desc_ensemble[1]) * tolerance;
            
            desc_ensemble[0] = desc_ensemble[2] + reducer;
            desc_ensemble[1] = desc_ensemble[2] - reducer;
            
            desc_sync_ensembles.append(desc_ensemble);
            sync_ensembles.append([ index_desc ]);
        else:
            oscillator_captured = False;
            for index_ensemble in range(0, len(sync_ensembles), 1):
                if ( (desc_sync_ensembles[index_ensemble][0] > descriptors[index_desc][2]) and (desc_sync_ensembles[index_ensemble][1] < descriptors[index_desc][2])):
                    sync_ensembles[index_ensemble].append(index_desc);
                    oscillator_captured = True;
                    break;
                
            if (oscillator_captured is False):
                desc_ensemble = descriptors[index_desc];
                reducer = (desc_ensemble[0] - desc_ensemble[1]) * tolerance;
        
                desc_ensemble[0] = desc_ensemble[2] + reducer;
                desc_ensemble[1] = desc_ensemble[2] - reducer;
        
                desc_sync_ensembles.append(desc_ensemble);
                sync_ensembles.append([ index_desc ]);
    
    return sync_ensembles;