def get_lock(self, token, key=None):
        """Return lock_dict, or None, if not found or invalid.

        Side effect: if lock is expired, it will be purged and None is returned.

        key:
            name of lock attribute that will be returned instead of a dictionary.
        """
        assert key in (
            None,
            "type",
            "scope",
            "depth",
            "owner",
            "root",
            "timeout",
            "principal",
            "token",
        )
        lock = self.storage.get(token)
        if key is None or lock is None:
            return lock
        return lock[key]