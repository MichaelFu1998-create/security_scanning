async def _update_loop(self) -> None:
        """Schedule a state update to keep the connection alive"""
        await asyncio.sleep(self._update_interval)
        while not self._closed:
            await self.update()
            await asyncio.sleep(self._update_interval)