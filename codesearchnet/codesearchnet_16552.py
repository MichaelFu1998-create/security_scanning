def sync_update_info(self, *_):
        """Update home info."""
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.update_info())
        loop.run_until_complete(task)