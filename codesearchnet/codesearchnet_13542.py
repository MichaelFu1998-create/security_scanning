def _bind_success(self, stanza):
        """Handle resource binding success.

        [initiating entity only]

        :Parameters:
            - `stanza`: <iq type="result"/> stanza received.

        Set `streambase.StreamBase.me` to the full JID negotiated."""
        # pylint: disable-msg=R0201
        payload = stanza.get_payload(ResourceBindingPayload)
        jid = payload.jid
        if not jid:
            raise BadRequestProtocolError(u"<jid/> element mising in"
                                                    " the bind response")
        self.stream.me = jid
        self.stream.event(AuthorizedEvent(self.stream.me))