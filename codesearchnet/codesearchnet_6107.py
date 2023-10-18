def element_content_as_string(element):
    """Serialize etree.Element.

    Note: element may contain more than one child or only text (i.e. no child
          at all). Therefore the resulting string may raise an exception, when
          passed back to etree.XML().
    """
    if len(element) == 0:
        return element.text or ""  # Make sure, None is returned as ''
    stream = compat.StringIO()
    for childnode in element:
        stream.write(xml_to_bytes(childnode, pretty_print=False) + "\n")
        # print(xml_to_bytes(childnode, pretty_print=False), file=stream)
    s = stream.getvalue()
    stream.close()
    return s