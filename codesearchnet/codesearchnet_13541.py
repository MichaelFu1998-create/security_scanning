def bind(self, stream, resource):
        """Bind to a resource.

        [initiating entity only]

        :Parameters:
            - `resource`: the resource name to bind to.
        :Types:
            - `resource`: `unicode`

        XMPP stream is authenticated for bare JID only. To use
        the full JID it must be bound to a resource.
        """
        self.stream = stream
        stanza = Iq(stanza_type = "set")
        payload = ResourceBindingPayload(resource = resource)
        stanza.set_payload(payload)
        self.stanza_processor.set_response_handlers(stanza,
                                        self._bind_success, self._bind_error)
        stream.send(stanza)
        stream.event(BindingResourceEvent(resource))