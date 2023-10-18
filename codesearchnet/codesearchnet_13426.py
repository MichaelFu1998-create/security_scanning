def unregister_fetcher(self, object_class):
        """Unregister a fetcher class for an object class.

        :Parameters:
            - `object_class`: class retrieved by the fetcher.
        :Types:
            - `object_class`: `classobj`
        """
        self._lock.acquire()
        try:
            cache = self._caches.get(object_class)
            if not cache:
                return
            cache.set_fetcher(None)
        finally:
            self._lock.release()