def _add_timeout_handler(self, handler):
        """Add a TimeoutHandler to the pool.
        """
        self.timeout_handlers.append(handler)
        if self.event_thread is None:
            return
        self._run_timeout_threads(handler)