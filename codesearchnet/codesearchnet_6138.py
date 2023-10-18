def refresh(self, token, timeout):
        """Modify an existing lock's timeout.

        token:
            Valid lock token.
        timeout:
            Suggested lifetime in seconds (-1 for infinite).
            The real expiration time may be shorter than requested!
        Returns:
            Lock dictionary.
            Raises ValueError, if token is invalid.
        """
        assert token in self._dict, "Lock must exist"
        assert timeout == -1 or timeout > 0
        if timeout < 0 or timeout > LockStorageDict.LOCK_TIME_OUT_MAX:
            timeout = LockStorageDict.LOCK_TIME_OUT_MAX

        self._lock.acquire_write()
        try:
            # Note: shelve dictionary returns copies, so we must reassign
            # values:
            lock = self._dict[token]
            lock["timeout"] = timeout
            lock["expire"] = time.time() + timeout
            self._dict[token] = lock
            self._flush()
        finally:
            self._lock.release()
        return lock