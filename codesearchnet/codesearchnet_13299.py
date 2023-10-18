def _roster_set(self, item, callback, error_callback):
        """Send a 'roster set' to the server.

        :Parameters:
            - `item`: the requested change
        :Types:
            - `item`: `RosterItem`
        """
        stanza = Iq(to_jid = self.server, stanza_type = "set")
        payload = RosterPayload([item])
        stanza.set_payload(payload)
        def success_cb(result_stanza):
            """Success callback for roster set."""
            if callback:
                callback(item)
        def error_cb(error_stanza):
            """Error callback for roster set."""
            if error_callback:
                error_callback(error_stanza)
            else:
                logger.error("Roster change of '{0}' failed".format(item.jid))
        processor = self.stanza_processor
        processor.set_response_handlers(stanza,
                                    success_cb, error_cb)
        processor.send(stanza)