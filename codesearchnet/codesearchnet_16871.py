def create_snippet(self, name, body, timeout=None):
        """ API call to create a Snippet """
        payload = {
            'name': name,
            'body': body
        }
        return self._api_request(
            self.SNIPPETS_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )