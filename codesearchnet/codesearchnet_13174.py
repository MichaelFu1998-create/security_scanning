def get_top_players(self, location_id='global', **params: keys):
        """Get a list of top players

        Parameters
        ----------
        location_id: Optional[str] = 'global'
            A location ID or global
            See https://github.com/RoyaleAPI/cr-api-data/blob/master/json/regions.json
            for a list of acceptable location IDs
        \*\*limit: Optional[int] = None
            Limit the number of items returned in the response
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.LOCATIONS + '/' + str(location_id) + '/rankings/players'
        return self._get_model(url, PartialPlayerClan, **params)