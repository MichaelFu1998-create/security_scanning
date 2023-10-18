def register_fetcher(self, object_class, fetcher_class):
        """Register a fetcher class for an object class.

        :Parameters:
            - `object_class`: class to be retrieved by the fetcher.
            - `fetcher_class`: the fetcher class.
        :Types:
            - `object_class`: `classobj`
            - `fetcher_class`: `CacheFetcher` based class
        """
        self._lock.acquire()
        try:
            cache = self._caches.get(object_class)
            if not cache:
                cache = Cache(self.max_items, self.default_freshness_period,
                        self.default_expiration_period, self.default_purge_period)
                self._caches[object_class] = cache
            cache.set_fetcher(fetcher_class)
        finally:
            self._lock.release()