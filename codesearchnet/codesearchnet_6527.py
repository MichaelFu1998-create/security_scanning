def delete(self, url, name, params=None, headers=None, connection=None):
        """
        Synchronous DELETE request. ``data`` must be a JSONable value.
        """
        if not name: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        return make_delete_request(endpoint, params, headers, connection=connection)