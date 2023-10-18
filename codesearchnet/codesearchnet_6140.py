def get_lock_list(self, path, include_root, include_children, token_only):
        """Return a list of direct locks for <path>.

        Expired locks are *not* returned (but may be purged).

        path:
            Normalized path (utf8 encoded string, no trailing '/')
        include_root:
            False: don't add <path> lock (only makes sense, when include_children
            is True).
        include_children:
            True: Also check all sub-paths for existing locks.
        token_only:
            True: only a list of token is returned. This may be implemented
            more efficiently by some providers.
        Returns:
            List of valid lock dictionaries (may be empty).
        """
        assert compat.is_native(path)
        assert path and path.startswith("/")
        assert include_root or include_children

        def __appendLocks(toklist):
            # Since we can do this quickly, we use self.get() even if
            # token_only is set, so expired locks are purged.
            for token in toklist:
                lock = self.get(token)
                if lock:
                    if token_only:
                        lockList.append(lock["token"])
                    else:
                        lockList.append(lock)

        path = normalize_lock_root(path)
        self._lock.acquire_read()
        try:
            key = "URL2TOKEN:{}".format(path)
            tokList = self._dict.get(key, [])
            lockList = []
            if include_root:
                __appendLocks(tokList)

            if include_children:
                for u, ltoks in self._dict.items():
                    if util.is_child_uri(key, u):
                        __appendLocks(ltoks)

            return lockList
        finally:
            self._lock.release()