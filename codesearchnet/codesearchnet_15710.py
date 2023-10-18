def post(self, url, headers=None, params=None, **kwargs):
        """Send a JSON POST request with the given request headers, additional
        URL query parameters, and the given JSON in the request body.  The
        extra query parameters are merged with any which already exist in the
        URL.  The 'json' and 'data' parameters may not both be given.

        Args:
            url (str): URL to retrieve
            headers (dict): Any other headers to be added to the request.
            params: dictionary or bytes to be sent in the query string for the
                request. (optional)
            json: json to send in the body of the Request.  This must be a
                JSON-serializable object. (optional)
            data: raw request body data.  May be a dictionary, list of tuples,
                bytes, or file-like object to send in the body of the Request.
                (optional)
        """

        if len(kwargs) > 1:
            raise InvalidArgumentsError("Too many extra args ({} > 1)".format(
                len(kwargs)))

        if kwargs:
            kwarg = next(iter(kwargs))
            if kwarg not in ("json", "data"):
                raise InvalidArgumentsError("Invalid kwarg: " + kwarg)

        resp = self.session.post(url, headers=headers, params=params, **kwargs)
        resp.raise_for_status()
        return _to_json(resp)