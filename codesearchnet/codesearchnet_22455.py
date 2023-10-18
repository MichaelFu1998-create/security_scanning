def invalidate_cache(self):
        """
        Invalidate httpBL cache
        """

        if self._use_cache:
            self._cache_version += 1
            self._cache.increment('cached_httpbl_{0}_version'.format(self._api_key))