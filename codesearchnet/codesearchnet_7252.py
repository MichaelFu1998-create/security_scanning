async def listen(self):
        """Listen for messages on the backwards channel.

        This method only returns when the connection has been closed due to an
        error.
        """
        retries = 0  # Number of retries attempted so far
        need_new_sid = True  # whether a new SID is needed

        while retries <= self._max_retries:
            # After the first failed retry, back off exponentially longer after
            # each attempt.
            if retries > 0:
                backoff_seconds = self._retry_backoff_base ** retries
                logger.info('Backing off for %s seconds', backoff_seconds)
                await asyncio.sleep(backoff_seconds)

            # Request a new SID if we don't have one yet, or the previous one
            # became invalid.
            if need_new_sid:
                await self._fetch_channel_sid()
                need_new_sid = False
            # Clear any previous push data, since if there was an error it
            # could contain garbage.
            self._chunk_parser = ChunkParser()
            try:
                await self._longpoll_request()
            except ChannelSessionError as err:
                logger.warning('Long-polling interrupted: %s', err)
                need_new_sid = True
            except exceptions.NetworkError as err:
                logger.warning('Long-polling request failed: %s', err)
            else:
                # The connection closed successfully, so reset the number of
                # retries.
                retries = 0
                continue

            retries += 1
            logger.info('retry attempt count is now %s', retries)
            if self._is_connected:
                self._is_connected = False
                await self.on_disconnect.fire()

            # If the request ended with an error, the client must account for
            # messages being dropped during this time.

        logger.error('Ran out of retries for long-polling request')