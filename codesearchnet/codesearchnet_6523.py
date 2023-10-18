def put_async(self, url, name, data, callback=None, params=None, headers=None):
        """
        Asynchronous PUT request with the process pool.
        """
        if name is None: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        process_pool.apply_async(make_put_request,
                                 args=(endpoint, data, params, headers),
                                 callback=callback)