def stream_request(self, method, url, headers=None, _session=None,
                       *args, **kwargs):
        """
            Make requests to the Streaming API

        Parameters
        ----------
        method : str
            Method to be used by the request
        url : str
            URL of the resource
        headers : dict
            Custom headers (doesn't overwrite `Authorization` headers)
        _session : aiohttp.ClientSession, optional
            The session to use for this specific request, the session
            given as argument of :meth:`__init__` is used by default

        Returns
        -------
        .stream.StreamResponse
            Stream context for the request
        """
        return StreamResponse(
            method=method,
            url=url,
            client=self,
            headers=headers,
            session=_session,
            proxy=self.proxy,
            **kwargs
        )