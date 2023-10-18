def serialize(element):
    """Serialize an XMPP element.

    Utility function for debugging or logging.

        :Parameters:
            - `element`: the element to serialize
        :Types:
            - `element`: :etree:`ElementTree.Element`

        :Return: serialized element
        :Returntype: `unicode`
    """
    if getattr(_THREAD, "serializer", None) is None:
        _THREAD.serializer = XMPPSerializer("jabber:client")
        _THREAD.serializer.emit_head(None, None)
    return _THREAD.serializer.emit_stanza(element)