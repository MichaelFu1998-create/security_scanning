def _finish(self, forced=False):
        """ Cleanup code after asked to stop producing.

        Kwargs:
            forced (bool): If True, we were forced to stop
        """
        if hasattr(self, "_current_file_handle") and self._current_file_handle:
            self._current_file_handle.close()
        
        if self._current_deferred:
            self._current_deferred.callback(self._sent)
            self._current_deferred = None

        if not forced and self._deferred:
            self._deferred.callback(self._sent)