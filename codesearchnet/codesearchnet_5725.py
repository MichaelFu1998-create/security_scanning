def _expires_in(self):
        """Return the number of seconds until this token expires.

        If token_expiry is in the past, this method will return 0, meaning the
        token has already expired.

        If token_expiry is None, this method will return None. Note that
        returning 0 in such a case would not be fair: the token may still be
        valid; we just don't know anything about it.
        """
        if self.token_expiry:
            now = _UTCNOW()
            if self.token_expiry > now:
                time_delta = self.token_expiry - now
                # TODO(orestica): return time_delta.total_seconds()
                # once dropping support for Python 2.6
                return time_delta.days * 86400 + time_delta.seconds
            else:
                return 0