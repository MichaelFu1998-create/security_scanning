def _request(self, failure, endpoints, *args, **kwargs):
        """
        Recursively make requests to each endpoint in ``endpoints``.
        """
        # We've run out of endpoints, fail
        if not endpoints:
            return failure

        endpoint = endpoints.pop(0)
        d = super(MarathonClient, self).request(*args, url=endpoint, **kwargs)

        # If something goes wrong, call ourselves again with the remaining
        # endpoints
        d.addErrback(self._request, endpoints, *args, **kwargs)
        return d