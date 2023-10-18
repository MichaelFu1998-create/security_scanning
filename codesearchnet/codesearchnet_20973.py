def validate_xml_text(text):
    """validates XML text"""
    bad_chars = __INVALID_XML_CHARS & set(text)
    if bad_chars:
        for offset,c in enumerate(text):
            if c in bad_chars:
                raise RuntimeError('invalid XML character: ' + repr(c) + ' at offset ' + str(offset))