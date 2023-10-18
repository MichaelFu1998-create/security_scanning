def get_player_verify(self, tag: crtag, apikey: str, timeout=None):
        """Check the API Key of a player.
        This endpoint has been **restricted** to
        certain members of the community

        Raises BadRequest if the apikey is invalid

        Parameters
        ----------
        tag: str
            A valid tournament tag. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        apikey: str
            The API Key in the player's settings
        timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.PLAYER + '/' + tag + '/verifytoken'
        return self._get_model(url, FullPlayer, timeout=timeout, method='POST', json={'token': apikey})