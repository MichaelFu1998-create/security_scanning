def write(self, path, **data):
        """
        Write data to Vault. Returns the JSON-decoded response.
        """
        d = self.request('PUT', '/v1/' + path, json=data)
        return d.addCallback(self._handle_response, check_cas=True)