async def seek(self, pos: int):
        """ Seeks to a given position in the track. """
        await self._lavalink.ws.send(op='seek', guildId=self.guild_id, position=pos)