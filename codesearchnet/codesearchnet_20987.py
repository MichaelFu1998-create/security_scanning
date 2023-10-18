def _close(self, conn):
        """Release waiters."""
        super(PooledAIODatabase, self)._close(conn)
        for waiter in self._waiters:
            if not waiter.done():
                logger.debug('Release a waiter')
                waiter.set_result(True)
                break