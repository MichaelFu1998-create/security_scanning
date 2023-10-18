async def async_connect(self):
        """Asyncronously wait for a connection from the pool."""
        if self._waiters is None:
            raise Exception('Error, database not properly initialized before async connection')

        if self._waiters or self.max_connections and (len(self._in_use) >= self.max_connections):
            waiter = asyncio.Future(loop=self._loop)
            self._waiters.append(waiter)

            try:
                logger.debug('Wait for connection.')
                await waiter
            finally:
                self._waiters.remove(waiter)

        self.connect()
        return self._state.conn