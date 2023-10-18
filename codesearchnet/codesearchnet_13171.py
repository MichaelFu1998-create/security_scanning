def get_all_locations(self, timeout: int=None):
        """Get a list of all locations

        Parameters
        ----------
        timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.LOCATIONS
        return self._get_model(url, timeout=timeout)