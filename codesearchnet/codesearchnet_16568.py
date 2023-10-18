def sync_get_historic_data(self, n_data):
        """get_historic_data."""
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.get_historic_data(n_data))
        loop.run_until_complete(task)
        return self._data