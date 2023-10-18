def _generate_lock(
        self, principal, lock_type, lock_scope, lock_depth, lock_owner, path, timeout
    ):
        """Acquire lock and return lock_dict.

        principal
            Name of the principal.
        lock_type
            Must be 'write'.
        lock_scope
            Must be 'shared' or 'exclusive'.
        lock_depth
            Must be '0' or 'infinity'.
        lock_owner
            String identifying the owner.
        path
            Resource URL.
        timeout
            Seconds to live

        This function does NOT check, if the new lock creates a conflict!
        """
        if timeout is None:
            timeout = LockManager.LOCK_TIME_OUT_DEFAULT
        elif timeout < 0:
            timeout = -1

        lock_dict = {
            "root": path,
            "type": lock_type,
            "scope": lock_scope,
            "depth": lock_depth,
            "owner": lock_owner,
            "timeout": timeout,
            "principal": principal,
        }
        #
        self.storage.create(path, lock_dict)
        return lock_dict