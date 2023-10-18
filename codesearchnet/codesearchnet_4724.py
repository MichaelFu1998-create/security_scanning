def __store_dynamic(self, dyn_phase, dyn_time, analyser, begin_state):
        """!
        @brief Store specified state of Sync network to hSync.
        
        @param[in] dyn_phase (list): Output dynamic of hSync where state should be stored.
        @param[in] dyn_time (list): Time points that correspond to output dynamic where new time point should be stored.
        @param[in] analyser (syncnet_analyser): Sync analyser where Sync states are stored.
        @param[in] begin_state (bool): If True the first state of Sync network is stored, otherwise the last state is stored.
        
        """
        
        if (begin_state is True):
            dyn_time.append(0);
            dyn_phase.append(analyser.output[0]);
        
        else:
            dyn_phase.append(analyser.output[len(analyser.output) - 1]);
            dyn_time.append(len(dyn_time));