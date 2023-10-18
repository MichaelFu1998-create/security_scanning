def fetch_raw(self, method, url, params=None, headers=None, data=None):
        """Make an HTTP request using aiohttp directly.

        Automatically uses configured HTTP proxy, and adds Google authorization
        header and cookies.

        Args:
            method (str): Request method.
            url (str): Request URL.
            params (dict): (optional) Request query string parameters.
            headers (dict): (optional) Request headers.
            data: (str): (optional) Request body data.

        Returns:
            aiohttp._RequestContextManager: ContextManager for a HTTP response.

        Raises:
            See ``aiohttp.ClientSession.request``.
        """
        # Ensure we don't accidentally send the authorization header to a
        # non-Google domain:
        if not urllib.parse.urlparse(url).hostname.endswith('.google.com'):
            raise Exception('expected google.com domain')

        headers = headers or {}
        headers.update(self._authorization_headers)
        return self._session.request(
            method, url, params=params, headers=headers, data=data,
            proxy=self._proxy
        )