def get_request_header(self):
        """Return ``request_header`` for use when constructing requests.

        Returns:
            Populated request header.
        """
        # resource is allowed to be null if it's not available yet (the Chrome
        # client does this for the first getentitybyid call)
        if self._client_id is not None:
            self._request_header.client_identifier.resource = self._client_id
        return self._request_header