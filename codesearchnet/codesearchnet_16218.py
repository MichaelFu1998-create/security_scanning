def execute(self, command, data={}):
        """Format the endpoint url by data and then request the remote server.

        Args:
            command(Command): WebDriver command to be executed.
            data(dict): Data fulfill the uri template and json body.

        Returns:
            A dict represent the json body from server response.

        Raises:
            KeyError: Data cannot fulfill the variable which command needed.
            ConnectionError: Meet network problem (e.g. DNS failure,
                refused connection, etc).
            Timeout: A request times out.
            HTTPError: HTTP request returned an unsuccessful status code.
        """
        method, uri = command
        try:
            path = self._formatter.format_map(uri, data)
            body = self._formatter.get_unused_kwargs()
            url = "{0}{1}".format(self._url, path)
            return self._request(method, url, body)
        except KeyError as err:
            LOGGER.debug(
                'Endpoint {0} is missing argument {1}'.format(uri, err))
            raise