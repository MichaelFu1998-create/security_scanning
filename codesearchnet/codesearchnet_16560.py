def sync_update_price_info(self):
        """Update current price info."""
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.update_price_info())
        loop.run_until_complete(task)