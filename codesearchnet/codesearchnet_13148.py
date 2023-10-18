def get_clan(self, *tags: crtag, **params: keys):
        """Get a clan information

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
        url = self.api.CLAN + '/' + ','.join(tags)
        return self._get_model(url, FullClan, **params)