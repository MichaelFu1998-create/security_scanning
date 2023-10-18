def route_stanza(self, stanza):
        """Process stanza not addressed to us.

        Return "recipient-unavailable" return if it is not
        "error" nor "result" stanza.

        This method should be overriden in derived classes if they
        are supposed to handle stanzas not addressed directly to local
        stream endpoint.

        :Parameters:
            - `stanza`: presence stanza to be processed
        """
        if stanza.stanza_type not in ("error", "result"):
            response = stanza.make_error_response(u"recipient-unavailable")
            self.send(response)
        return True