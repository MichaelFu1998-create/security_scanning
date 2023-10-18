def init_async(self, loop):
        """Initialize self."""
        super(PooledAIODatabase, self).init_async(loop)
        self._waiters = collections.deque()