def request(self, path, data=None, headers=None, method=None):
        """Performs a HTTP request to the Go server

        Args:
          path (str): The full path on the Go server to request.
            This includes any query string attributes.
          data (str, dict, bool, optional): If any data is present this
            request will become a POST request.
          headers (dict, optional): Headers to set for this particular
            request

        Raises:
          HTTPError: when the HTTP request fails.

        Returns:
          file like object: The response from a
            :func:`urllib2.urlopen` call
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        response = urlopen(self._request(path, data=data, headers=headers, method=method))
        self._set_session_cookie(response)

        return response