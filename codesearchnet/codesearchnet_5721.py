def has_scopes(self, scopes):
        """Verify that the credentials are authorized for the given scopes.

        Returns True if the credentials authorized scopes contain all of the
        scopes given.

        Args:
            scopes: list or string, the scopes to check.

        Notes:
            There are cases where the credentials are unaware of which scopes
            are authorized. Notably, credentials obtained and stored before
            this code was added will not have scopes, AccessTokenCredentials do
            not have scopes. In both cases, you can use refresh_scopes() to
            obtain the canonical set of scopes.
        """
        scopes = _helpers.string_to_scopes(scopes)
        return set(scopes).issubset(self.scopes)