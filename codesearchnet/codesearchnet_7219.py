async def consume(self):
        """Consume coroutines from the queue by executing them."""
        while True:
            coro = await self._queue.get()
            assert asyncio.iscoroutine(coro)
            await coro