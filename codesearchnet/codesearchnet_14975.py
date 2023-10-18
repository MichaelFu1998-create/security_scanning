def create_access_token(self, valid_in_hours=1, data=None):
        """
        Creates an access token.

        TODO: check valid in hours
        TODO: maybe specify how often a token can be used
        """
        data = data or {}
        token = AccessToken(
            token=self.generate(),
            expires_at=expires_at(hours=valid_in_hours),
            data=data)
        return token