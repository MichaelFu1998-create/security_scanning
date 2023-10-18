def get(self, key, delete_if_expired=True):
        """
        Retrieve key from Cache.

        :param key: key to look up in cache.
        :type key: ``object``

        :param delete_if_expired: remove value from cache if it is expired.
                                  Default is True.
        :type delete_if_expired: ``bool``

        :returns: value from cache or None
        :rtype: varies or None
        """
        self._update_cache_stats(key, None)

        if key in self._CACHE:
            (expiration, obj) = self._CACHE[key]
            if expiration > self._now():
                self._update_cache_stats(key, 'hit')
                return obj
            else:
                if delete_if_expired:
                    self.delete(key)
                    self._update_cache_stats(key, 'expired')
                    return None
    
        self._update_cache_stats(key, 'miss')
        return None