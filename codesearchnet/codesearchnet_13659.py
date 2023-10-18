def _reset(self):
        """Reset the `LegacyClientStream` object state, making the object ready
        to handle new connections."""
        ClientStream._reset(self)
        self.available_auth_methods = None
        self.auth_stanza = None
        self.registration_callback = None