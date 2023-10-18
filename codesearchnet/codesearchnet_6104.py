def string_to_xml(text):
    """Convert XML string into etree.Element."""
    try:
        return etree.XML(text)
    except Exception:
        # TODO:
        # ExpatError: reference to invalid character number: line 1, column 62
        # litmus fails, when xml is used instead of lxml
        # 18. propget............... FAIL (PROPFIND on `/temp/litmus/prop2':
        #   Could not read status line: connection was closed by server)
        # text = <ns0:high-unicode xmlns:ns0="http://example.com/neon/litmus/">&#55296;&#56320;
        #   </ns0:high-unicode>
        #        t2 = text.encode("utf8")
        #        return etree.XML(t2)
        _logger.error(
            "Error parsing XML string. "
            "If lxml is not available, and unicode is involved, then "
            "installing lxml _may_ solve this issue."
        )
        _logger.error("XML source: {}".format(text))
        raise