async def async_connect(self):
        """Catch a connection asyncrounosly."""
        if self._async_lock is None:
            raise Exception('Error, database not properly initialized before async connection')

        async with self._async_lock:
            self.connect(True)

        return self._state.conn