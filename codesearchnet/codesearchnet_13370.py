def _stream_authorized(self, event):
        """Handle the `AuthorizedEvent`.
        """
        with self.lock:
            if event.stream != self.stream:
                return
            self.me = event.stream.me
            self.peer = event.stream.peer
            presence = self.settings[u"initial_presence"]
            if presence:
                self.send(presence)