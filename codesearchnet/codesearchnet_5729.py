def _revoke(self, http):
        """Revokes this credential and deletes the stored copy (if it exists).

        Args:
            http: an object to be used to make HTTP requests.
        """
        self._do_revoke(http, self.refresh_token or self.access_token)