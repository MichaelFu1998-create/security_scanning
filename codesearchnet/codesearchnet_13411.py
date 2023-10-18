def error(self, error_data):
        """Handle a retrieval error and call apriopriate handler.

        Should be called when retrieval fails.

        Do nothing when the fetcher is not active any more (after
        one of handlers was already called).

        :Parameters:
            - `error_data`: additional information about the error (e.g. `StanzaError` instance).
        :Types:
            - `error_data`: fetcher dependant
        """
        if not self.active:
            return
        if not self._try_backup_item():
            self._error_handler(self.address, error_data)
        self.cache.invalidate_object(self.address)
        self._deactivate()