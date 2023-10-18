def get_user(self):
        """
        Method that gets the authenticated user. The returning user has
        the token, email and the provider data.
        """
        token = self.authenticator.create_token(self.extra)
        user_id = self.extra.get('id')
        return FirebaseUser(self.email, token, self.provider, user_id)