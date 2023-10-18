def fetch_request_token(self, url, realm=None, **request_kwargs):
        r"""Fetch a request token.

        This is the first step in the OAuth 1 workflow. A request token is
        obtained by making a signed post request to url. The token is then
        parsed from the application/x-www-form-urlencoded response and ready
        to be used to construct an authorization url.

        :param url: The request token endpoint URL.
        :param realm: A list of realms to request access to.
        :param \*\*request_kwargs: Optional arguments passed to ''post''
        function in ''requests.Session''
        :returns: The response in dict format.

        Note that a previously set callback_uri will be reset for your
        convenience, or else signature creation will be incorrect on
        consecutive requests.

        >>> request_token_url = 'https://api.twitter.com/oauth/request_token'
        >>> oauth_session = OAuth1Session('client-key', client_secret='secret')
        >>> oauth_session.fetch_request_token(request_token_url)
        {
            'oauth_token': 'sdf0o9823sjdfsdf',
            'oauth_token_secret': '2kjshdfp92i34asdasd',
        }
        """
        self._client.client.realm = " ".join(realm) if realm else None
        token = self._fetch_token(url, **request_kwargs)
        log.debug("Resetting callback_uri and realm (not needed in next phase).")
        self._client.client.callback_uri = None
        self._client.client.realm = None
        return token