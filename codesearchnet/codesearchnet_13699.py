def uplink_receive(self, stanza):
        """Handle stanza received from the stream."""
        with self.lock:
            if self.stanza_route:
                self.stanza_route.uplink_receive(stanza)
            else:
                logger.debug(u"Stanza dropped (no route): {0!r}".format(stanza))