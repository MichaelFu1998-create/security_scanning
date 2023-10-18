def get_url_lock_list(self, url):
        """Return list of lock_dict, if <url> is protected by at least one direct, valid lock.

        Side effect: expired locks for this url are purged.
        """
        url = normalize_lock_root(url)
        lockList = self.storage.get_lock_list(
            url, include_root=True, include_children=False, token_only=False
        )
        return lockList