def _add_timeout_handler(self, handler):
        """Add a `TimeoutHandler` to the main loop."""
        # pylint: disable=W0212
        for dummy, method in inspect.getmembers(handler, callable):
            if not hasattr(method, "_pyxmpp_timeout"):
                continue
            tag = glib.timeout_add(int(method._pyxmpp_timeout * 1000),
                                                self._timeout_cb, method)
            self._timer_sources[method] = tag