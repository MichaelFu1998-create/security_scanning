def _run_timeout_threads(self, handler):
        """Start threads for a TimeoutHandler.
        """
        # pylint: disable-msg=W0212
        for dummy, method in inspect.getmembers(handler, callable):
            if not hasattr(method, "_pyxmpp_timeout"):
                continue
            thread = TimeoutThread(method, daemon = self.daemon,
                                                    exc_queue = self.exc_queue)
            self.timeout_threads.append(thread)
            thread.start()