def get_snippet(self, snippet_id, timeout=None):
        """ API call to get a specific Snippet """
        return self._api_request(
            self.SNIPPET_ENDPOINT % (snippet_id),
            self.HTTP_GET,
            timeout=timeout
        )