def set_peer_authenticated(self, peer, restart_stream = False):
        """Mark the other side of the stream authenticated as `peer`

        :Parameters:
            - `peer`: local JID just authenticated
            - `restart_stream`: `True` when stream should be restarted (needed
              after SASL authentication)
        :Types:
            - `peer`: `JID`
            - `restart_stream`: `bool`
        """
        with self.lock:
            self.peer_authenticated = True
            self.peer = peer
            if restart_stream:
                self._restart_stream()
        self.event(AuthenticatedEvent(self.peer))