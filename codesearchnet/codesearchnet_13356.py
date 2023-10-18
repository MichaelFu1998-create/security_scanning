def _remove_timeout_handler(self, handler):
        """Remove `TimeoutHandler` from the main loop."""
        self._timeout_handlers = [(t, h) for (t, h)
                                            in self._timeout_handlers
                                            if h.im_self != handler]