async def update_state(self, data):
        """ Updates a player's state when a payload with opcode ``playerUpdate`` is received. """
        guild_id = int(data['guildId'])

        if guild_id in self.players:
            player = self.players.get(guild_id)
            player.position = data['state'].get('position', 0)
            player.position_timestamp = data['state']['time']