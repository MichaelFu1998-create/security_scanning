def _authenticate(self, params, headers):
        """
        Method that simply adjusts authentication credentials for the
        request.
        `params` is the querystring of the request.
        `headers` is the header of the request.

        If auth instance is not provided to this class, this method simply
        returns without doing anything.
        """
        if self.authentication:
            user = self.authentication.get_user()
            params.update({'auth': user.firebase_auth_token})
            headers.update(self.authentication.authenticator.HEADERS)