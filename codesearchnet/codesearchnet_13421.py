def remove_fetcher(self, fetcher):
        """Remove a running fetcher from the list of active fetchers.

        :Parameters:
            - `fetcher`: fetcher instance.
        :Types:
            - `fetcher`: `CacheFetcher`"""
        self._lock.acquire()
        try:
            for t, f in list(self._active_fetchers):
                if f is fetcher:
                    self._active_fetchers.remove((t, f))
                    f._deactivated()
                    return
        finally:
            self._lock.release()