async def disconnect(self, code):
        """
        default is to wait for the child applications to close.
        """
        try:
            await asyncio.wait(
                self.application_futures.values(),
                return_when=asyncio.ALL_COMPLETED,
                timeout=self.application_close_timeout
            )
        except asyncio.TimeoutError:
            pass