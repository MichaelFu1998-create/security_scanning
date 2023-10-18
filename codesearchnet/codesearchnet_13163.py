def get_player_battles(self, tag: crtag, **params: keys):
        """Get a player's battle log

        Parameters
        ----------
        tag: str
            A valid tournament tag. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        \*\*limit: Optional[int] = None
            Limit the number of items returned in the response
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.PLAYER + '/' + tag + '/battlelog'
        return self._get_model(url, **params)