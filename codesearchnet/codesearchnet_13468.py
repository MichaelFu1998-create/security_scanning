def _stanza_handler(element_name, stanza_type, payload_class, payload_key,
                                                            usage_restriction):
    """Method decorator generator for decorating <message/> or <presence/>
    stanza handler methods in `XMPPFeatureHandler` subclasses.

    :Parameters:
        - `element_name`: "message" or "presence"
        - `stanza_type`: expected value of the 'type' attribute of the stanza
        - `payload_class`: payload class expected
        - `payload_key`: payload class specific filtering key
        - `usage_restriction`: optional usage restriction: "pre-auth" or
          "post-auth"
    :Types:
        - `element_name`: `unicode`
        - `stanza_type`: `unicode`
        - `payload_class`: subclass of `StanzaPayload`
        - `usage_restriction`: `unicode`
    """
    def decorator(func):
        """The decorator"""
        func._pyxmpp_stanza_handled = (element_name, stanza_type)
        func._pyxmpp_payload_class_handled = payload_class
        func._pyxmpp_payload_key = payload_key
        func._pyxmpp_usage_restriction = usage_restriction
        return func
    return decorator