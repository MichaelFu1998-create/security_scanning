def xml_to_bytes(element, pretty_print=False):
    """Wrapper for etree.tostring, that takes care of unsupported pretty_print
    option and prepends an encoding header."""
    if use_lxml:
        xml = etree.tostring(
            element, encoding="UTF-8", xml_declaration=True, pretty_print=pretty_print
        )
    else:
        xml = etree.tostring(element, encoding="UTF-8")
        if not xml.startswith(b"<?xml "):
            xml = b'<?xml version="1.0" encoding="utf-8" ?>\n' + xml

    assert xml.startswith(b"<?xml ")  # ET should prepend an encoding header
    return xml