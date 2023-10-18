def put(self, coro):
        """Put a coroutine in the queue to be executed."""
        # Avoid logging when a coroutine is queued or executed to avoid log
        # spam from coroutines that are started on every keypress.
        assert asyncio.iscoroutine(coro)
        self._queue.put_nowait(coro)