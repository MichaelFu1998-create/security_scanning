async def stop(self):
        """ Stops the player, if playing. """
        await self._lavalink.ws.send(op='stop', guildId=self.guild_id)
        self.current = None