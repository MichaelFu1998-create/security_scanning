def make_error_response(self, cond):
        """Create error response for the a "get" or "set" iq stanza.

        :Parameters:
            - `cond`: error condition name, as defined in XMPP specification.

        :return: new `Iq` object with the same "id" as self, "from" and "to"
            attributes swapped, type="error" and containing <error /> element
            plus payload of `self`.
        :returntype: `Iq`"""

        if self.stanza_type in ("result", "error"):
            raise ValueError("Errors may not be generated for"
                                                " 'result' and 'error' iq")

        stanza = Iq(stanza_type="error", from_jid = self.to_jid,
                        to_jid = self.from_jid, stanza_id = self.stanza_id,
                        error_cond = cond)
        if self._payload is None:
            self.decode_payload()
        for payload in self._payload:
            # use Stanza.add_payload to skip the payload length check
            Stanza.add_payload(stanza, payload)
        return stanza