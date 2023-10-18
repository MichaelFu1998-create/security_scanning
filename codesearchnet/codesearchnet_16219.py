def _request(self, method, url, body):
        """Internal method to send request to the remote server.

        Args:
            method(str): HTTP Method(GET/POST/PUT/DELET/HEAD).
            url(str): The request url.
            body(dict): The JSON object to be sent.

        Returns:
            A dict represent the json body from server response.

        Raises:
            ConnectionError: Meet network problem (e.g. DNS failure,
                refused connection, etc).
            Timeout: A request times out.
            HTTPError: HTTP request returned an unsuccessful status code.
        """
        if method != 'POST' and method != 'PUT':
            body = None

        s = Session()

        LOGGER.debug(
            'Method: {0}, Url: {1}, Body: {2}.'.format(method, url, body))

        req = Request(method, url, json=body)
        prepped = s.prepare_request(req)

        res = s.send(prepped, timeout=self._timeout or None)
        res.raise_for_status()
        # TODO try catch
        return res.json()