def get_known_tournaments(self, **params: tournamentfilter):
        """Get a list of queried tournaments

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
        url = self.api.TOURNAMENT + '/known'
        return self._get_model(url, PartialTournament, **params)