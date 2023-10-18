async def set_pause(self, pause: bool):
        """ Sets the player's paused state. """
        await self._lavalink.ws.send(op='pause', guildId=self.guild_id, pause=pause)
        self.paused = pause