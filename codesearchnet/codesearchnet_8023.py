async def on_socket_response(self, data):
        """
        This coroutine will be called every time an event from Discord is received.
        It is used to update a player's voice state through forwarding a payload via the WebSocket connection to Lavalink.
        -------------
        :param data:
            The payload received from Discord.
        """

        # INTERCEPT VOICE UPDATES
        if not data or data.get('t', '') not in ['VOICE_STATE_UPDATE', 'VOICE_SERVER_UPDATE']:
            return

        if data['t'] == 'VOICE_SERVER_UPDATE':
            self.voice_state.update({
                'op': 'voiceUpdate',
                'guildId': data['d']['guild_id'],
                'event': data['d']
            })
        else:
            if int(data['d']['user_id']) != self.bot.user.id:
                return

            self.voice_state.update({'sessionId': data['d']['session_id']})

            guild_id = int(data['d']['guild_id'])

            if self.players[guild_id]:
                self.players[guild_id].channel_id = data['d']['channel_id']

        if {'op', 'guildId', 'sessionId', 'event'} == self.voice_state.keys():
            await self.ws.send(**self.voice_state)
            self.voice_state.clear()