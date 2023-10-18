def make_error_response(self, cond):
        """Create error response for the any non-error presence stanza.

        :Parameters:
            - `cond`: error condition name, as defined in XMPP specification.
        :Types:
            - `cond`: `unicode`

        :return: new presence stanza.
        :returntype: `Presence`
        """

        if self.stanza_type == "error":
            raise ValueError("Errors may not be generated in response"
                                                                " to errors")

        stanza = Presence(stanza_type = "error", from_jid = self.from_jid,
                            to_jid = self.to_jid, stanza_id = self.stanza_id,
                            status = self._status, show = self._show,
                            priority = self._priority, error_cond = cond)

        if self._payload is None:
            self.decode_payload()

        for payload in self._payload:
            stanza.add_payload(payload)

        return stanza