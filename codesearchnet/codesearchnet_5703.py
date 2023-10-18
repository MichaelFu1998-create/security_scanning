def get_access_token(self, http=None, additional_claims=None):
        """Create a signed jwt.

        Args:
            http: unused
            additional_claims: dict, additional claims to add to
                the payload of the JWT.
        Returns:
            An AccessTokenInfo with the signed jwt
        """
        if additional_claims is None:
            if self.access_token is None or self.access_token_expired:
                self.refresh(None)
            return client.AccessTokenInfo(
              access_token=self.access_token, expires_in=self._expires_in())
        else:
            # Create a 1 time token
            token, unused_expiry = self._create_token(additional_claims)
            return client.AccessTokenInfo(
              access_token=token, expires_in=self._MAX_TOKEN_LIFETIME_SECS)