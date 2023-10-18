async def listen(self):
        """ Waits to receive a payload from the Lavalink server and processes it. """
        while not self._shutdown:
            try:
                data = json.loads(await self._ws.recv())
            except websockets.ConnectionClosed as error:
                log.warning('Disconnected from Lavalink: {}'.format(str(error)))
                for g in self._lavalink.players._players.copy().keys():
                    ws = self._lavalink.bot._connection._get_websocket(int(g))
                    await ws.voice_state(int(g), None)

                self._lavalink.players.clear()

                if self._shutdown:
                    break

                if await self._attempt_reconnect():
                    return

                log.warning('Unable to reconnect to Lavalink!')
                break

            op = data.get('op', None)
            log.debug('Received WebSocket data {}'.format(str(data)))

            if not op:
                return log.debug('Received WebSocket message without op {}'.format(str(data)))

            if op == 'event':
                log.debug('Received event of type {}'.format(data['type']))
                player = self._lavalink.players[int(data['guildId'])]
                event = None

                if data['type'] == 'TrackEndEvent':
                    event = TrackEndEvent(player, data['track'], data['reason'])
                elif data['type'] == 'TrackExceptionEvent':
                    event = TrackExceptionEvent(player, data['track'], data['error'])
                elif data['type'] == 'TrackStuckEvent':
                    event = TrackStuckEvent(player, data['track'], data['thresholdMs'])

                if event:
                    await self._lavalink.dispatch_event(event)
            elif op == 'playerUpdate':
                await self._lavalink.update_state(data)
            elif op == 'stats':
                self._lavalink.stats._update(data)
                await self._lavalink.dispatch_event(StatsUpdateEvent(self._lavalink.stats))

        log.debug('Closing WebSocket...')
        await self._ws.close()