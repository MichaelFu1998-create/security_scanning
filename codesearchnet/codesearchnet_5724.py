def get_access_token(self, http=None):
        """Return the access token and its expiration information.

        If the token does not exist, get one.
        If the token expired, refresh it.
        """
        if not self.access_token or self.access_token_expired:
            if not http:
                http = transport.get_http_object()
            self.refresh(http)
        return AccessTokenInfo(access_token=self.access_token,
                               expires_in=self._expires_in())