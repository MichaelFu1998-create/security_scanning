def get(self, guild_id):
        """ Returns a player from the cache, or creates one if it does not exist. """
        if guild_id not in self._players:
            p = self._player(lavalink=self.lavalink, guild_id=guild_id)
            self._players[guild_id] = p

        return self._players[guild_id]