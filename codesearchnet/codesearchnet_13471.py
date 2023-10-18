def payload_element_name(element_name):
    """Class decorator generator for decorationg
    `StanzaPayload` subclasses.

    :Parameters:
        - `element_name`: XML element qname handled by the class
    :Types:
        - `element_name`: `unicode`
    """
    def decorator(klass):
        """The payload_element_name decorator."""
        # pylint: disable-msg=W0212,W0404
        from .stanzapayload import STANZA_PAYLOAD_CLASSES
        from .stanzapayload import STANZA_PAYLOAD_ELEMENTS
        if hasattr(klass, "_pyxmpp_payload_element_name"):
            klass._pyxmpp_payload_element_name.append(element_name)
        else:
            klass._pyxmpp_payload_element_name = [element_name]
        if element_name in STANZA_PAYLOAD_CLASSES:
            logger = logging.getLogger('pyxmpp.payload_element_name')
            logger.warning("Overriding payload class for {0!r}".format(
                                                                element_name))
        STANZA_PAYLOAD_CLASSES[element_name] = klass
        STANZA_PAYLOAD_ELEMENTS[klass].append(element_name)
        return klass
    return decorator