async def connect(self):
        """Establish a connection to the chat server.

        Returns when an error has occurred, or :func:`disconnect` has been
        called.
        """
        proxy = os.environ.get('HTTP_PROXY')
        self._session = http_utils.Session(self._cookies, proxy=proxy)
        try:
            self._channel = channel.Channel(
                self._session, self._max_retries, self._retry_backoff_base
            )

            # Forward the Channel events to the Client events.
            self._channel.on_connect.add_observer(self.on_connect.fire)
            self._channel.on_reconnect.add_observer(self.on_reconnect.fire)
            self._channel.on_disconnect.add_observer(self.on_disconnect.fire)
            self._channel.on_receive_array.add_observer(self._on_receive_array)

            # Wrap the coroutine in a Future so it can be cancelled.
            self._listen_future = asyncio.ensure_future(self._channel.listen())
            # Listen for StateUpdate messages from the Channel until it
            # disconnects.
            try:
                await self._listen_future
            except asyncio.CancelledError:
                # If this task is cancelled, we need to cancel our child task
                # as well. We don't need an additional yield because listen
                # cancels immediately.
                self._listen_future.cancel()
            logger.info(
                'Client.connect returning because Channel.listen returned'
            )
        finally:
            await self._session.close()