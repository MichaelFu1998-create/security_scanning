def get_player_chests(self, tag: crtag, timeout: int=None):
        """Get information about a player's chest cycle

        Parameters
        ----------
        tag: str
            A valid tournament tag. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.PLAYER + '/' + tag + '/upcomingchests'
        return self._get_model(url, timeout=timeout)