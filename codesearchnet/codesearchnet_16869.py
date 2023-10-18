def snippets(self, timeout=None):
        """ API call to get list of snippets """
        return self._api_request(
            self.SNIPPETS_ENDPOINT,
            self.HTTP_GET,
            timeout=timeout
        )