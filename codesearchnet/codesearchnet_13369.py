def _stream_authenticated(self, event):
        """Handle the `AuthenticatedEvent`.
        """
        with self.lock:
            if event.stream != self.stream:
                return
            self.me = event.stream.me
            self.peer = event.stream.peer
            handlers = self._base_handlers[:]
            handlers += self.handlers + [self]
            self.setup_stanza_handlers(handlers, "post-auth")