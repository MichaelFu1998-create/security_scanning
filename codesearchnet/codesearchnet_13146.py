def get_player_verify(self, tag: crtag, apikey: str, **params: keys):
        """Check the API Key of a player.
        This endpoint has been **restricted** to
        certain members of the community

        Parameters
        ----------
        tag: str
            A valid tournament tag. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        apikey: str
            The API Key in the player's settings
        \*\*keys: Optional[list] = None
            Filter which keys should be included in the
            response
        \*\*exclude: Optional[list] = None
            Filter which keys should be excluded from the
            response
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.PLAYER + '/' + tag + '/verify'
        params.update({'token': apikey})
        return self._get_model(url, FullPlayer, **params)