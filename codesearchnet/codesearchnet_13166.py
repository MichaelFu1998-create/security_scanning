def search_clans(self, **params: clansearch):
        """Search for a clan. At least one
        of the filters must be present

        Parameters
        ----------
        name: Optional[str]
            The name of a clan
            (has to be at least 3 characters long)
        locationId: Optional[int]
            A location ID
        minMembers: Optional[int]
            The minimum member count
            of a clan
        maxMembers: Optional[int]
            The maximum member count
            of a clan
        minScore: Optional[int]
            The minimum trophy score of
            a clan
        \*\*limit: Optional[int] = None
            Limit the number of items returned in the response
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.CLAN
        return self._get_model(url, PartialClan, **params)