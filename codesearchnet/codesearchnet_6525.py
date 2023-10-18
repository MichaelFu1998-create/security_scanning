def post_async(self, url, data, callback=None, params=None, headers=None):
        """
        Asynchronous POST request with the process pool.
        """
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        process_pool.apply_async(make_post_request,
                                 args=(endpoint, data, params, headers),
                                 callback=callback)