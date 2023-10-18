def process_configuration_success(self, stanza):
        """
        Process success response for a room configuration request.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `Presence`
        """
        _unused = stanza
        self.configured = True
        self.handler.room_configured()