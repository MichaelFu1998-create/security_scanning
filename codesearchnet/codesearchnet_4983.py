def calculate_local_sync_order(oscillator_phases, oscillatory_network):
        """!
        @brief Calculates level of local synchorization (local order parameter) for input phases for the specified network.
        @details This parameter is tend 1.0 when the oscillatory network close to local synchronization and it tend to 0.0 when 
                  desynchronization is observed in the network.
        
        @param[in] oscillator_phases (list): List of oscillator phases that are used for level of local (partial) synchronization.
        @param[in] oscillatory_network (sync): Instance of oscillatory network whose connections are required for calculation.
        
        @return (double) Level of local synchronization (local order parameter).
        
        """
        
        exp_amount = 0.0;
        num_neigh = 0.0;
        
        for i in range(0, len(oscillatory_network), 1):
            for j in range(0, len(oscillatory_network), 1):
                if (oscillatory_network.has_connection(i, j) == True):
                    exp_amount += math.exp(-abs(oscillator_phases[j] - oscillator_phases[i]));
                    num_neigh += 1.0;
        
        if (num_neigh == 0):
            num_neigh = 1.0;
        
        return exp_amount / num_neigh;