def request(self, method, url=None, **kwargs):
        """
        Perform a request.

        :param: method:
            The HTTP method to use (example is `GET`).
        :param: url:
            The URL to use. The default value is the URL this client was
            created with (`self.url`) (example is `http://localhost:8080`)
        :param: kwargs:
            Any other parameters that will be passed to `treq.request`, for
            example headers. Or any URL parameters to override, for example
            path, query or fragment.
        """
        url = self._compose_url(url, kwargs)

        kwargs.setdefault('timeout', self._timeout)

        d = self._client.request(method, url, reactor=self._reactor, **kwargs)

        d.addCallback(self._log_request_response, method, url, kwargs)
        d.addErrback(self._log_request_error, url)

        return d