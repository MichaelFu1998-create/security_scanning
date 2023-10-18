def url(self):
        """
        Return the URL of the server.

        :returns: URL of the server
        :rtype: string
        """
        if len(self.drivers) > 0:
            return self.drivers[0].url
        else:
            return self._url