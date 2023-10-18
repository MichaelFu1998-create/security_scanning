def _deactivate(self):
        """Remove the fetcher from cache and mark it not active."""
        self.cache.remove_fetcher(self)
        if self.active:
            self._deactivated()