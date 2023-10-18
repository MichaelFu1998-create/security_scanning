async def await_event(self, event=None, timeout=None):
        """ Wait for any or specified event """
        if self.event_future is not None:
            raise Exception("Can't wait on multiple events!")

        result = await asyncio.wait_for(self._wait_loop(event), timeout)
        return result