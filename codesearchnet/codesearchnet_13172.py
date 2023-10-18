def get_location(self, location_id: int, timeout: int=None):
        """Get a location information

        Parameters
        ----------
        location_id: int
            A location ID
            See https://github.com/RoyaleAPI/cr-api-data/blob/master/json/regions.json
            for a list of acceptable location IDs
        timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.LOCATIONS + '/' + str(location_id)
        return self._get_model(url, timeout=timeout)