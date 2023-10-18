def output(self):
        """!
        @brief (list) Returns output dynamic of the Sync network (phase coordinates of each oscillator in the network) during simulation.
        
        """
        if ( (self._ccore_sync_dynamic_pointer is not None) and ( (self._dynamic is None) or (len(self._dynamic) == 0) ) ):
            self._dynamic = wrapper.sync_dynamic_get_output(self._ccore_sync_dynamic_pointer);
        
        return self._dynamic;