def handle_authorized(self, event):
        """Send session esteblishment request if the feature was advertised by
        the server.
        """
        stream = event.stream
        if not stream:
            return
        if not stream.initiator:
            return
        if stream.features is None:
            return
        element = stream.features.find(SESSION_TAG)
        if element is None:
            return
        logger.debug("Establishing IM session")
        stanza = Iq(stanza_type = "set")
        payload = XMLPayload(ElementTree.Element(SESSION_TAG))
        stanza.set_payload(payload)
        self.stanza_processor.set_response_handlers(stanza,
                                        self._session_success,
                                        self._session_error)
        stream.send(stanza)