def read(self, path, **params):
        """
        Read data from Vault. Returns the JSON-decoded response.
        """
        d = self.request('GET', '/v1/' + path, params=params)
        return d.addCallback(self._handle_response)