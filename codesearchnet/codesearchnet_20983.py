def init_async(self, loop=None):
        """Use when application is starting."""
        self._loop = loop or asyncio.get_event_loop()
        self._async_lock = asyncio.Lock(loop=loop)

        # FIX: SQLITE in memory database
        if not self.database == ':memory:':
            self._state = ConnectionLocal()