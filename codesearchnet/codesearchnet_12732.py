async def _connect(self):
        """
            Connect to the stream

        Returns
        -------
        asyncio.coroutine
            The streaming response
        """
        logger.debug("connecting to the stream")
        await self.client.setup
        if self.session is None:
            self.session = self.client._session
        kwargs = await self.client.headers.prepare_request(**self.kwargs)
        request = self.client.error_handler(self.session.request)

        return await request(timeout=0, **kwargs)