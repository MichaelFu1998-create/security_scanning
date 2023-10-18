def get_async(self, url, name, callback=None, params=None, headers=None):
        """
        Asynchronous GET request with the process pool.
        """
        if name is None: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        process_pool.apply_async(make_get_request,
            args=(endpoint, params, headers), callback=callback)