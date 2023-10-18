def get(self, url, name, params=None, headers=None, connection=None):
        """
        Synchronous GET request.
        """
        if name is None: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        return make_get_request(endpoint, params, headers, connection=connection)