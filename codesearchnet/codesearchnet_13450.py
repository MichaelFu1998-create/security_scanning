def add_handler(self, handler):
        """Add a handler object.

        :Parameters:
            - `handler`: the object providing event handler methods
        :Types:
            - `handler`: `EventHandler`
        """
        if not isinstance(handler, EventHandler):
            raise TypeError, "Not an EventHandler"
        with self.lock:
            if handler in self.handlers:
                return
            self.handlers.append(handler)
            self._update_handlers()