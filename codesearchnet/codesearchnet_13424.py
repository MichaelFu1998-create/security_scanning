def tick(self):
        """Do the regular cache maintenance.

        Must be called from time to time for timeouts and cache old items
        purging to work."""
        self._lock.acquire()
        try:
            for cache in self._caches.values():
                cache.tick()
        finally:
            self._lock.release()