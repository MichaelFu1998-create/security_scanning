def access_token_expired(self):
        """True if the credential is expired or invalid.

        If the token_expiry isn't set, we assume the token doesn't expire.
        """
        if self.invalid:
            return True

        if not self.token_expiry:
            return False

        now = _UTCNOW()
        if now >= self.token_expiry:
            logger.info('access_token is expired. Now: %s, token_expiry: %s',
                        now, self.token_expiry)
            return True
        return False