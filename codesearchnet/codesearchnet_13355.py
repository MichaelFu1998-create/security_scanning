def _add_timeout_handler(self, handler):
        """Add a `TimeoutHandler` to the main loop."""
        # pylint: disable-msg=W0212
        now = time.time()
        for dummy, method in inspect.getmembers(handler, callable):
            if not hasattr(method, "_pyxmpp_timeout"):
                continue
            self._timeout_handlers.append((now + method._pyxmpp_timeout,
                                                                    method))
        self._timeout_handlers.sort(key = lambda x: x[0])