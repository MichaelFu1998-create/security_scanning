def set_authenticated(self, me, restart_stream = False):
        """Mark stream authenticated as `me`.

        :Parameters:
            - `me`: local JID just authenticated
            - `restart_stream`: `True` when stream should be restarted (needed
              after SASL authentication)
        :Types:
            - `me`: `JID`
            - `restart_stream`: `bool`
        """
        with self.lock:
            self.authenticated = True
            self.me = me
            if restart_stream:
                self._restart_stream()
        self.event(AuthenticatedEvent(self.me))