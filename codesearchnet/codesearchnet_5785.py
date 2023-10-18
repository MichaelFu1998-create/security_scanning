def _create_flow(self, request_handler):
        """Create the Flow object.

        The Flow is calculated lazily since we don't know where this app is
        running until it receives a request, at which point redirect_uri can be
        calculated and then the Flow object can be constructed.

        Args:
            request_handler: webapp.RequestHandler, the request handler.
        """
        if self.flow is None:
            redirect_uri = request_handler.request.relative_url(
                self._callback_path)  # Usually /oauth2callback
            self.flow = client.OAuth2WebServerFlow(
                self._client_id, self._client_secret, self._scope,
                redirect_uri=redirect_uri, user_agent=self._user_agent,
                auth_uri=self._auth_uri, token_uri=self._token_uri,
                revoke_uri=self._revoke_uri, **self._kwargs)