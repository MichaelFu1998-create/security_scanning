def get_clan_tracking(self, *tags: crtag, **params: keys):
        """Returns if the clan is currently being tracked
        by the API by having either cr-api.com or royaleapi.com
        in the clan description

        Parameters
        ----------
        \*tags: str
            Valid clan tags. Minimum length: 3
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
        url = self.api.CLAN + '/' + ','.join(tags) + '/tracking'
        return self._get_model(url, **params)