def get_clan(self, tag: crtag, timeout: int=None):
        """Get inforamtion about a clan

        Parameters
        ----------
        tag: str
            A valid tournament tag. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.CLAN + '/' + tag
        return self._get_model(url, FullClan, timeout=timeout)