def is_url_locked_by_token(self, url, lock_token):
        """Check, if url (or any of it's parents) is locked by lock_token."""
        lockUrl = self.get_lock(lock_token, "root")
        return lockUrl and util.is_equal_or_child_uri(lockUrl, url)