def get_player_battles(self, *tags: crtag, **params: keys):
        """Get a player's battle log

        Parameters
        ----------
        \*tags: str
            Valid player tags. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        \*\*keys: Optional[list] = None
            Filter which keys should be included in the
            response
        \*\*exclude: Optional[list] = None
            Filter which keys should be excluded from the
            response
        \*\*max: Optional[int] = None
            Limit the number of items returned in the response
        \*\*page: Optional[int] = None
            Works with max, the zero-based page of the
            items
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.PLAYER + '/' + ','.join(tags) + '/battles'
        return self._get_model(url, **params)