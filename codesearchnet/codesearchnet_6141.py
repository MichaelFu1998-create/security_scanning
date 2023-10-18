def _flush(self):
        """Write persistent dictionary to disc."""
        _logger.debug("_flush()")
        self._lock.acquire_write()  # TODO: read access is enough?
        try:
            self._dict.sync()
        finally:
            self._lock.release()