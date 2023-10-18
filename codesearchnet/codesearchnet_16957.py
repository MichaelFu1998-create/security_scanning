def set_scheduled(self):
        """
        Returns True if state was successfully changed from idle to scheduled.
        """
        with self._idle_lock:
            if self._idle:
                self._idle = False
                return True
        return False