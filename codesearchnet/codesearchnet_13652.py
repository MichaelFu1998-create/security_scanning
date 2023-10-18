def _remove_io_handler(self, handler):
        """Remove an IOHandler from the pool.
        """
        if handler not in self.io_handlers:
            return
        self.io_handlers.remove(handler)
        for thread in self.io_threads:
            if thread.io_handler is handler:
                thread.stop()