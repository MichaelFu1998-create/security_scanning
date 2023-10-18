def remove_handler(self, handler):
        """Remove a handler object.

        :Parameters:
            - `handler`: the object to remove
        """
        with self.lock:
            if handler in self.handlers:
                self.handlers.remove(handler)
                self._update_handlers()