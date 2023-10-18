def request_software_version(stanza_processor, target_jid, callback,
                                                    error_callback = None):
    """Request software version information from a remote entity.

    When a valid response is received the `callback` will be handled
    with a `VersionPayload` instance as its only argument. The object will
    provide the requested infromation.

    In case of error stanza received or invalid response the `error_callback`
    (if provided) will be called with the offending stanza (which can
    be ``<iq type='error'/>`` or ``<iq type='result'>``) as its argument.

    The same function will be called on timeout, with the argument set to
    `None`.

    :Parameters:
        - `stanza_processor`: a object used to send the query and handle
          response. E.g. a `pyxmpp2.client.Client` instance
        - `target_jid`: the JID of the entity to query
        - `callback`: function to be called with a valid response
        - `error_callback`: function to be called on error
    :Types:
        - `stanza_processor`: `StanzaProcessor`
        - `target_jid`: `JID`
    """
    stanza = Iq(to_jid = target_jid, stanza_type = "get")
    payload = VersionPayload()
    stanza.set_payload(payload)
    def wrapper(stanza):
        """Wrapper for the user-provided `callback` that extracts the payload
        from stanza received."""
        payload = stanza.get_payload(VersionPayload)
        if payload is None:
            if error_callback:
                error_callback(stanza)
            else:
                logger.warning("Invalid version query response.")
        else:
            callback(payload)
    stanza_processor.set_response_handlers(stanza, wrapper, error_callback)
    stanza_processor.send(stanza)