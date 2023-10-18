def acquire(
        self,
        url,
        lock_type,
        lock_scope,
        lock_depth,
        lock_owner,
        timeout,
        principal,
        token_list,
    ):
        """Check for permissions and acquire a lock.

        On success return new lock dictionary.
        On error raise a DAVError with an embedded DAVErrorCondition.
        """
        url = normalize_lock_root(url)
        self._lock.acquire_write()
        try:
            # Raises DAVError on conflict:
            self._check_lock_permission(
                url, lock_type, lock_scope, lock_depth, token_list, principal
            )
            return self._generate_lock(
                principal, lock_type, lock_scope, lock_depth, lock_owner, url, timeout
            )
        finally:
            self._lock.release()