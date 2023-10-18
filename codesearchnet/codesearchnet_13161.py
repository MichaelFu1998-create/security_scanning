def get_player(self, tag: crtag, timeout=None):
        """Get information about a player

        Parameters
        ----------
        tag: str
            A valid tournament tag. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.PLAYER + '/' + tag
        return self._get_model(url, FullPlayer, timeout=timeout)