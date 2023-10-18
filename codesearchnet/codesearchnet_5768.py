def email(self):
        """Returns the user's email address or None if there are no credentials.

        The email address is provided by the current credentials' id_token.
        This should not be used as unique identifier as the user can change
        their email. If you need a unique identifier, use user_id.
        """
        if not self.credentials:
            return None
        try:
            return self.credentials.id_token['email']
        except KeyError:
            current_app.logger.error(
                'Invalid id_token {0}'.format(self.credentials.id_token))