def _refresh(self, http):
        """Refreshes the access token.

        Since the underlying App Engine app_identity implementation does its
        own caching we can skip all the storage hoops and just to a refresh
        using the API.

        Args:
            http: unused HTTP object

        Raises:
            AccessTokenRefreshError: When the refresh fails.
        """
        try:
            scopes = self.scope.split()
            (token, _) = app_identity.get_access_token(
                scopes, service_account_id=self.service_account_id)
        except app_identity.Error as e:
            raise client.AccessTokenRefreshError(str(e))
        self.access_token = token