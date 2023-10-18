def has_credentials(self):
        """Returns True if there are valid credentials for the current user
        and required scopes."""
        credentials = _credentials_from_request(self.request)
        return (credentials and not credentials.invalid and
                credentials.has_scopes(self._get_scopes()))