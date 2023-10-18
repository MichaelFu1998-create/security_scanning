def calculate_sync_order(oscillator_phases):
        """!
        @brief Calculates level of global synchronization (order parameter) for input phases.
        @details This parameter is tend 1.0 when the oscillatory network close to global synchronization and it tend to 0.0 when 
                  desynchronization is observed in the network.
        
        @param[in] oscillator_phases (list): List of oscillator phases that are used for level of global synchronization.
        
        @return (double) Level of global synchronization (order parameter).
        
        @see calculate_order_parameter()
        
        """
        
        exp_amount = 0.0;
        average_phase = 0.0;

        for phase in oscillator_phases:
            exp_amount += math.expm1( abs(1j * phase) );
            average_phase += phase;
        
        exp_amount /= len(oscillator_phases);
        average_phase = math.expm1( abs(1j * (average_phase / len(oscillator_phases))) );
        
        return abs(average_phase) / abs(exp_amount);