async def connect(self):
        """ Establishes a connection to the Lavalink server. """
        await self._lavalink.bot.wait_until_ready()

        if self._ws and self._ws.open:
            log.debug('WebSocket still open, closing...')
            await self._ws.close()

        user_id = self._lavalink.bot.user.id
        shard_count = self._lavalink.bot.shard_count or self._shards

        headers = {
            'Authorization': self._password,
            'Num-Shards': shard_count,
            'User-Id': str(user_id)
        }
        log.debug('Preparing to connect to Lavalink')
        log.debug('    with URI: {}'.format(self._uri))
        log.debug('    with headers: {}'.format(str(headers)))
        log.info('Connecting to Lavalink...')

        try:
            self._ws = await websockets.connect(self._uri, loop=self._loop, extra_headers=headers)
        except OSError as error:
            log.exception('Failed to connect to Lavalink: {}'.format(str(error)))
        else:
            log.info('Connected to Lavalink!')
            self._loop.create_task(self.listen())
            version = self._ws.response_headers.get('Lavalink-Major-Version', 2)
            try:
                self._lavalink._server_version = int(version)
            except ValueError:
                self._lavalink._server_version = 2
            log.info('Lavalink server version is {}'.format(version))
            if self._queue:
                log.info('Replaying {} queued events...'.format(len(self._queue)))
                for task in self._queue:
                    await self.send(**task)