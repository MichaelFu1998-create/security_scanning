def post(self, url, data, params=None, headers=None, connection=None):
        """
        Synchronous POST request. ``data`` must be a JSONable value.
        """
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        return make_post_request(endpoint, data, params, headers,
                                 connection=connection)