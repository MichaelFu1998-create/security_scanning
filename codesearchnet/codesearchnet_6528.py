def delete_async(self, url, name, callback=None, params=None, headers=None):
        """
        Asynchronous DELETE request with the process pool.
        """
        if not name: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        process_pool.apply_async(make_delete_request,
                    args=(endpoint, params, headers), callback=callback)