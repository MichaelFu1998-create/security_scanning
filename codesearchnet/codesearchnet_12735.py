async def restart_stream(self):
        """
            Restart the stream on error
        """
        await self.response.release()
        await asyncio.sleep(self._error_timeout)
        await self.connect()

        logger.info("Reconnected to the stream")
        self._reconnecting = False
        return {'stream_restart': True}