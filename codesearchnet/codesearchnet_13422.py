def set_fetcher(self, fetcher_class):
        """Set the fetcher class.

        :Parameters:
            - `fetcher_class`: the fetcher class.
        :Types:
            - `fetcher_class`: `CacheFetcher` based class
        """
        self._lock.acquire()
        try:
            self._fetcher = fetcher_class
        finally:
            self._lock.release()