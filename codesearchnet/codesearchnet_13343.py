def process_iq(self, stanza):
        """Process IQ stanza received.

        :Parameters:
            - `stanza`: the stanza received
        :Types:
            - `stanza`: `Iq`

        If a matching handler is available pass the stanza to it.  Otherwise
        ignore it if it is "error" or "result" stanza or return
        "feature-not-implemented" error if it is "get" or "set"."""

        typ = stanza.stanza_type
        if typ in ("result", "error"):
            return self._process_iq_response(stanza)
        if typ not in ("get", "set"):
            raise BadRequestProtocolError("Bad <iq/> type")
        logger.debug("Handling <iq type='{0}'> stanza: {1!r}".format(
                                                            stanza, typ))
        payload = stanza.get_payload(None)
        logger.debug("  payload: {0!r}".format(payload))
        if not payload:
            raise BadRequestProtocolError("<iq/> stanza with no child element")
        handler = self._get_iq_handler(typ, payload)
        if not handler:
            payload = stanza.get_payload(None, specialize = True)
            logger.debug("  specialized payload: {0!r}".format(payload))
            if not isinstance(payload, XMLPayload):
                handler = self._get_iq_handler(typ, payload)
        if handler:
            response = handler(stanza)
            self._process_handler_result(response)
            return True
        else:
            raise ServiceUnavailableProtocolError("Not implemented")