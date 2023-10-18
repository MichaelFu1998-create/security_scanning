def _request(self, endpoint, *args, **kwargs):
        """
        Perform a request to a specific endpoint. Raise an error if the status
        code indicates a client or server error.
        """
        kwargs['url'] = endpoint
        return (super(MarathonLbClient, self).request(*args, **kwargs)
                .addCallback(raise_for_status))