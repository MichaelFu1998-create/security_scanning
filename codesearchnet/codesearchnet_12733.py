async def connect(self):
        """
            Create the connection

        Returns
        -------
        self

        Raises
        ------
        exception.PeonyException
            On a response status in 4xx that are not status 420 or 429
            Also on statuses in 1xx or 3xx since this should not be the status
            received here
        """
        with async_timeout.timeout(self.timeout):
            self.response = await self._connect()

        if self.response.status in range(200, 300):
            self._error_timeout = 0
            self.state = NORMAL
        elif self.response.status == 500:
            self.state = DISCONNECTION
        elif self.response.status in range(501, 600):
            self.state = RECONNECTION
        elif self.response.status in (420, 429):
            self.state = ENHANCE_YOUR_CALM
        else:
            logger.debug("raising error during stream connection")
            raise await exceptions.throw(self.response,
                                         loads=self.client._loads,
                                         url=self.kwargs['url'])

        logger.debug("stream state: %d" % self.state)