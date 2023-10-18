def _refresh(self, http):
        """Refreshes the access token.

        Skip all the storage hoops and just refresh using the API.

        Args:
            http: an object to be used to make HTTP requests.

        Raises:
            HttpAccessTokenRefreshError: When the refresh fails.
        """
        try:
            self._retrieve_info(http)
            self.access_token, self.token_expiry = _metadata.get_token(
                http, service_account=self.service_account_email)
        except http_client.HTTPException as err:
            raise client.HttpAccessTokenRefreshError(str(err))