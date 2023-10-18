def delete(self, token):
        """Delete lock.

        Returns True on success. False, if token does not exist, or is expired.
        """
        self._lock.acquire_write()
        try:
            lock = self._dict.get(token)
            _logger.debug("delete {}".format(lock_string(lock)))
            if lock is None:
                return False
            # Remove url to lock mapping
            key = "URL2TOKEN:{}".format(lock.get("root"))
            if key in self._dict:
                # _logger.debug("    delete token {} from url {}".format(token, lock.get("root")))
                tokList = self._dict[key]
                if len(tokList) > 1:
                    # Note: shelve dictionary returns copies, so we must
                    # reassign values:
                    tokList.remove(token)
                    self._dict[key] = tokList
                else:
                    del self._dict[key]
            # Remove the lock
            del self._dict[token]

            self._flush()
        finally:
            self._lock.release()
        return True