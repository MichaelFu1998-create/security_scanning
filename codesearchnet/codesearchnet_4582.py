def extract_number_oscillations(osc_dyn, index = 0, amplitude_threshold = 1.0):
    """!
    @brief Extracts number of oscillations of specified oscillator.
    
    @param[in] osc_dyn (list): Dynamic of oscillators.
    @param[in] index (uint): Index of oscillator in dynamic.
    @param[in] amplitude_threshold (double): Amplitude threshold when oscillation is taken into account, for example,
                when oscillator amplitude is greater than threshold then oscillation is incremented.
    
    @return (uint) Number of oscillations of specified oscillator.
    
    """
    
    number_oscillations = 0;
    waiting_differential = False;
    threshold_passed = False;
    high_level_trigger = True if (osc_dyn[0][index] > amplitude_threshold) else False;
    
    for values in osc_dyn:
        if ( (values[index] >= amplitude_threshold) and (high_level_trigger is False) ):
            high_level_trigger = True;
            threshold_passed = True;
        
        elif ( (values[index] < amplitude_threshold) and (high_level_trigger is True) ):
            high_level_trigger = False;
            threshold_passed = True;
        
        if (threshold_passed is True):
            threshold_passed = False;
            if (waiting_differential is True and high_level_trigger is False):
                number_oscillations += 1;
                waiting_differential = False;

            else:
                waiting_differential = True;
        
    return number_oscillations;