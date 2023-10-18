def _remove_timeout_handler(self, handler):
        """Remove `TimeoutHandler` from the main loop."""
        for dummy, method in inspect.getmembers(handler, callable):
            if not hasattr(method, "_pyxmpp_timeout"):
                continue
            tag = self._timer_sources.pop(method, None)
            if tag is not None:
                glib.source_remove(tag)