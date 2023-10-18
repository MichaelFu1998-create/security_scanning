def _remove_timeout_handler(self, handler):
        """Remove a TimeoutHandler from the pool.
        """
        if handler not in self.timeout_handlers:
            return
        self.timeout_handlers.remove(handler)
        for thread in self.timeout_threads:
            if thread.method.im_self is handler:
                thread.stop()