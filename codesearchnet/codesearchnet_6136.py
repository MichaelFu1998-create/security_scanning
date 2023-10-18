def get(self, token):
        """Return a lock dictionary for a token.

        If the lock does not exist or is expired, None is returned.

        token:
            lock token
        Returns:
            Lock dictionary or <None>

        Side effect: if lock is expired, it will be purged and None is returned.
        """
        self._lock.acquire_read()
        try:
            lock = self._dict.get(token)
            if lock is None:
                # Lock not found: purge dangling URL2TOKEN entries
                _logger.debug("Lock purged dangling: {}".format(token))
                self.delete(token)
                return None
            expire = float(lock["expire"])
            if expire >= 0 and expire < time.time():
                _logger.debug(
                    "Lock timed-out({}): {}".format(expire, lock_string(lock))
                )
                self.delete(token)
                return None
            return lock
        finally:
            self._lock.release()