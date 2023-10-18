def _refresh(self, http):
        """Refreshes the access_token.

        This method first checks by reading the Storage object if available.
        If a refresh is still needed, it holds the Storage lock until the
        refresh is completed.

        Args:
            http: an object to be used to make HTTP requests.

        Raises:
            HttpAccessTokenRefreshError: When the refresh fails.
        """
        if not self.store:
            self._do_refresh_request(http)
        else:
            self.store.acquire_lock()
            try:
                new_cred = self.store.locked_get()

                if (new_cred and not new_cred.invalid and
                        new_cred.access_token != self.access_token and
                        not new_cred.access_token_expired):
                    logger.info('Updated access_token read from Storage')
                    self._updateFromCredential(new_cred)
                else:
                    self._do_refresh_request(http)
            finally:
                self.store.release_lock()