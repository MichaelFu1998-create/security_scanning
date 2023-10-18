def _close_stream(self):
        """Same as `close_stream` but with the `lock` acquired.
        """
        self.stream.close()
        if self.stream.transport in self._ml_handlers:
            self._ml_handlers.remove(self.stream.transport)
            self.main_loop.remove_handler(self.stream.transport)
        self.stream = None
        self.uplink = None