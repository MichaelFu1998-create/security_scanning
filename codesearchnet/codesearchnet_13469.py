def message_stanza_handler(stanza_type = None, payload_class = None,
                        payload_key = None, usage_restriction = "post-auth"):
    """Method decorator generator for decorating <message/>
    stanza handler methods in `XMPPFeatureHandler` subclasses.

    :Parameters:
        - `payload_class`: payload class expected
        - `stanza_type`: expected value of the 'type' attribute of the stanza.
          `None` means all types except 'error'
        - `payload_key`: payload class specific filtering key
        - `usage_restriction`: optional usage restriction: "pre-auth" or
          "post-auth"
    :Types:
        - `payload_class`: subclass of `StanzaPayload`
        - `stanza_type`: `unicode`
        - `usage_restriction`: `unicode`
    """
    if stanza_type is None:
        stanza_type = "normal"
    return _stanza_handler("message", stanza_type, payload_class, payload_key,
                                                            usage_restriction)