def stream_element_handler(element_name, usage_restriction = None):
    """Method decorator generator for decorating stream element
    handler methods in `StreamFeatureHandler` subclasses.

    :Parameters:
        - `element_name`: stream element QName
        - `usage_restriction`: optional usage restriction: "initiator" or
          "receiver"
    :Types:
        - `element_name`: `unicode`
        - `usage_restriction`: `unicode`
    """
    def decorator(func):
        """The decorator"""
        func._pyxmpp_stream_element_handled = element_name
        func._pyxmpp_usage_restriction = usage_restriction
        return func
    return decorator