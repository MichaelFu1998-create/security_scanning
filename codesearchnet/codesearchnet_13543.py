def handle_bind_iq_set(self, stanza):
        """Handler <iq type="set"/> for resource binding."""
        # pylint: disable-msg=R0201
        if not self.stream:
            logger.error("Got bind stanza before stream feature has been set")
            return False
        if self.stream.initiator:
            return False
        peer = self.stream.peer
        if peer.resource:
            raise ResourceConstraintProtocolError(
                        u"Only one resource per client supported")
        resource = stanza.get_payload(ResourceBindingPayload).resource
        jid = None
        if resource:
            try:
                jid = JID(peer.local, peer.domain, resource)
            except JIDError:
                pass
        if jid is None:
            resource = unicode(uuid.uuid4())
            jid = JID(peer.local, peer.domain, resource)
        response = stanza.make_result_response()
        payload = ResourceBindingPayload(jid = jid)
        response.set_payload(payload)
        self.stream.peer = jid
        self.stream.event(AuthorizedEvent(jid))
        return response