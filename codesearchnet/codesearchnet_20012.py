async def _push(self, *args, **kwargs):
        """Push new data into the buffer. Resume looping if paused."""
        self._data.append((args, kwargs))
        if self._future is not None:

            future, self._future = self._future, None
            future.set_result(True)