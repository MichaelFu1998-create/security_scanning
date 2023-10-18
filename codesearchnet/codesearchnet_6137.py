def create(self, path, lock):
        """Create a direct lock for a resource path.

        path:
            Normalized path (utf8 encoded string, no trailing '/')
        lock:
            lock dictionary, without a token entry
        Returns:
            New unique lock token.: <lock

        **Note:** the lock dictionary may be modified on return:

        - lock['root'] is ignored and set to the normalized <path>
        - lock['timeout'] may be normalized and shorter than requested
        - lock['token'] is added
        """
        self._lock.acquire_write()
        try:
            # We expect only a lock definition, not an existing lock
            assert lock.get("token") is None
            assert lock.get("expire") is None, "Use timeout instead of expire"
            assert path and "/" in path

            # Normalize root: /foo/bar
            org_path = path
            path = normalize_lock_root(path)
            lock["root"] = path

            # Normalize timeout from ttl to expire-date
            timeout = float(lock.get("timeout"))
            if timeout is None:
                timeout = LockStorageDict.LOCK_TIME_OUT_DEFAULT
            elif timeout < 0 or timeout > LockStorageDict.LOCK_TIME_OUT_MAX:
                timeout = LockStorageDict.LOCK_TIME_OUT_MAX

            lock["timeout"] = timeout
            lock["expire"] = time.time() + timeout

            validate_lock(lock)

            token = generate_lock_token()
            lock["token"] = token

            # Store lock
            self._dict[token] = lock

            # Store locked path reference
            key = "URL2TOKEN:{}".format(path)
            if key not in self._dict:
                self._dict[key] = [token]
            else:
                # Note: Shelve dictionary returns copies, so we must reassign
                # values:
                tokList = self._dict[key]
                tokList.append(token)
                self._dict[key] = tokList
            self._flush()
            _logger.debug(
                "LockStorageDict.set({!r}): {}".format(org_path, lock_string(lock))
            )
            return lock
        finally:
            self._lock.release()