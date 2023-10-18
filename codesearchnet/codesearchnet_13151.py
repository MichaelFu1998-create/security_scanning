def get_clan_war(self, tag: crtag, **params: keys):
        """Get inforamtion about a clan's current clan war

        Parameters
        ----------
        *tag: str
            A valid clan tag. Minimum length: 3
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
        url = self.api.CLAN + '/' + tag + '/war'
        return self._get_model(url, **params)