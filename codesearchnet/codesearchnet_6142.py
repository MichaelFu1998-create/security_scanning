def clear(self):
        """Delete all entries."""
        self._lock.acquire_write()  # TODO: read access is enough?
        try:
            was_closed = self._dict is None
            if was_closed:
                self.open()
            if len(self._dict):
                self._dict.clear()
                self._dict.sync()
            if was_closed:
                self.close()
        finally:
            self._lock.release()