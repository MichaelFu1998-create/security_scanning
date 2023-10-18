def get_tournament(self, tag: crtag, **params: keys):
        """Get a tournament information

        Parameters
        ----------
        tag: str
            A valid tournament tag. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        \*\*keys: Optional[list] = None
            Filter which keys should be included in the
            response
        \*\*exclude: Optional[list] = None
            Filter which keys should be excluded from the
            response
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.TOURNAMENT + '/' + tag
        return self._get_model(url, **params)