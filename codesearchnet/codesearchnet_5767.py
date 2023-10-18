def has_credentials(self):
        """Returns True if there are valid credentials for the current user."""
        if not self.credentials:
            return False
        # Is the access token expired? If so, do we have an refresh token?
        elif (self.credentials.access_token_expired and
                not self.credentials.refresh_token):
            return False
        else:
            return True