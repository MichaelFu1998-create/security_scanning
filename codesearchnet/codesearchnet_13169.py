def search_tournaments(self, name: str, **params: keys):
        """Search for a tournament by its name

        Parameters
        ----------
        name: str
            The name of a tournament
        \*\*limit: Optional[int] = None
            Limit the number of items returned in the response
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.TOURNAMENT
        params['name'] = name
        return self._get_model(url, PartialTournament, **params)