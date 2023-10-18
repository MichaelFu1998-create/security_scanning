def make_error_response(self, cond):
        """Create error response for any non-error message stanza.

        :Parameters:
            - `cond`: error condition name, as defined in XMPP specification.

        :return: new message stanza with the same "id" as self, "from" and
            "to" attributes swapped, type="error" and containing <error />
            element plus payload of `self`.
        :returntype: `Message`"""

        if self.stanza_type == "error":
            raise ValueError("Errors may not be generated in response"
                                                                " to errors")

        msg = Message(stanza_type = "error", from_jid = self.to_jid,
                        to_jid = self.from_jid, stanza_id = self.stanza_id,
                        error_cond = cond,
                        subject = self._subject, body = self._body,
                        thread = self._thread)

        if self._payload is None:
            self.decode_payload()
        for payload in self._payload:
            msg.add_payload(payload.copy())

        return msg