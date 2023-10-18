def get_constants(self, **params: keys):
        """Get the CR Constants

        Parameters
        ----------
        \*\*keys: Optional[list] = None
            Filter which keys should be included in the
            response
        \*\*exclude: Optional[list] = None
            Filter which keys should be excluded from the
            response
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.CONSTANTS
        return self._get_model(url, **params)