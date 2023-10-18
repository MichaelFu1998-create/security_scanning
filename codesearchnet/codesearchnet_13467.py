def _iq_handler(iq_type, payload_class, payload_key, usage_restriction):
    """Method decorator generator for decorating <iq type='get'/> stanza
    handler methods in `XMPPFeatureHandler` subclasses.

    :Parameters:
        - `payload_class`: payload class expected
        - `payload_key`: payload class specific filtering key
        - `usage_restriction`: optional usage restriction: "pre-auth" or
          "post-auth"
    :Types:
        - `payload_class`: subclass of `StanzaPayload`
        - `usage_restriction`: `unicode`
    """
    def decorator(func):
        """The decorator"""
        func._pyxmpp_stanza_handled = ("iq", iq_type)
        func._pyxmpp_payload_class_handled = payload_class
        func._pyxmpp_payload_key = payload_key
        func._pyxmpp_usage_restriction = usage_restriction
        return func
    return decorator