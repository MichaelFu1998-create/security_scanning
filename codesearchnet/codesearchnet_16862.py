def templates(self, timeout=None):
        """ API call to get a list of templates """
        return self._api_request(
            self.TEMPLATES_ENDPOINT,
            self.HTTP_GET,
            timeout=timeout
        )