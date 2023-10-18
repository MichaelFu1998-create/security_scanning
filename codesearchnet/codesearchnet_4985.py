def time(self):
        """!
        @brief (list) Returns sampling times when dynamic is measured during simulation.
        
        """
        if ( (self._ccore_sync_dynamic_pointer is not None) and ( (self._time is None) or (len(self._time) == 0) ) ):
            self._time = wrapper.sync_dynamic_get_time(self._ccore_sync_dynamic_pointer);
        
        return self._time;