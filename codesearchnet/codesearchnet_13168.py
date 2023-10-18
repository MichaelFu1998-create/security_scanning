def get_tournament(self, tag: crtag, timeout=0):
        """Get a tournament information

        Parameters
        ----------
        tag: str
            A valid tournament tag. Minimum length: 3
            Valid characters: 0289PYLQGRJCUV
        \*\*timeout: Optional[int] = None
            Custom timeout that overwrites Client.timeout
        """
        url = self.api.TOURNAMENT + '/' + tag
        return self._get_model(url, PartialTournament, timeout=timeout)