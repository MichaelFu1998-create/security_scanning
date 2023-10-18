def element_to_unicode(element):
    """Serialize an XML element into a unicode string.

    This should work the same on Python2 and Python3 and with all
    :etree:`ElementTree` implementations.

    :Parameters:
        - `element`: the XML element to serialize
    :Types:
        - `element`: :etree:`ElementTree.Element`
    """
    if hasattr(ElementTree, 'tounicode'):
        # pylint: disable=E1103
        return ElementTree.tounicode("element")
    elif sys.version_info.major < 3:
        return unicode(ElementTree.tostring(element))
    else:
        return ElementTree.tostring(element, encoding = "unicode")