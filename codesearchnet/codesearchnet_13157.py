def get_popular_players(self, **params: keys):
        """Get a list of most queried players

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
        url = self.api.POPULAR + '/players'
        return self._get_model(url, PartialPlayerClan, **params)