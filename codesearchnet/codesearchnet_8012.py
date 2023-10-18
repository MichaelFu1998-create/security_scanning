def remove(self, guild_id):
        """ Removes a player from the current players. """
        if guild_id in self._players:
            self._players[guild_id].cleanup()
            del self._players[guild_id]