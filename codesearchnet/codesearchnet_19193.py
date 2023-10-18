def add_logged_in_session(self, response=None):
        """Make the request appear to be coming from a browser

        This is to interact with older parts of Go that doesn't have a
        proper API call to be made. What will be done:

        1. If no response passed in a call to `go/api/pipelines.xml` is
           made to get a valid session
        2. `JSESSIONID` will be populated from this request
        3. A request to `go/pipelines` will be so the
           `authenticity_token` (CSRF) can be extracted. It will then
           silently be injected into `post_args` on any POST calls that
           doesn't start with `go/api` from this point.

        Args:
          response: a :class:`Response` object from a previously successful
            API call. So we won't have to query `go/api/pipelines.xml`
            unnecessarily.

        Raises:
          HTTPError: when the HTTP request fails.
          AuthenticationFailed: when failing to get the `session_id`
            or the `authenticity_token`.
        """
        if not response:
            response = self.get('go/api/pipelines.xml')

        self._set_session_cookie(response)

        if not self._session_id:
            raise AuthenticationFailed('No session id extracted from request.')

        response = self.get('go/pipelines')
        match = re.search(
            r'name="authenticity_token".+?value="([^"]+)',
            response.read().decode('utf-8')
        )
        if match:
            self._authenticity_token = match.group(1)
        else:
            raise AuthenticationFailed('Authenticity token not found on page')