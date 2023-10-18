def _stream_disconnected(self, event):
        """Handle stream disconnection event.
        """
        with self.lock:
            if event.stream != self.stream:
                return
            if self.stream is not None and event.stream == self.stream:
                if self.stream.transport in self._ml_handlers:
                    self._ml_handlers.remove(self.stream.transport)
                    self.main_loop.remove_handler(self.stream.transport)
                self.stream = None
                self.uplink = None