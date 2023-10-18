def tick(self):
        """Do the regular cache maintenance.

        Must be called from time to time for timeouts and cache old items
        purging to work."""
        self._lock.acquire()
        try:
            now = datetime.utcnow()
            for t,f in list(self._active_fetchers):
                if t > now:
                    break
                f.timeout()
            self.purge_items()
        finally:
            self._lock.release()