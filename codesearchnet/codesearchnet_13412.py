def timeout(self):
        """Handle fetcher timeout and call apriopriate handler.

        Is called by the cache object and should _not_ be called by fetcher or
        application.

        Do nothing when the fetcher is not active any more (after
        one of handlers was already called)."""
        if not self.active:
            return
        if not self._try_backup_item():
            if self._timeout_handler:
                self._timeout_handler(self.address)
            else:
                self._error_handler(self.address, None)
        self.cache.invalidate_object(self.address)
        self._deactivate()