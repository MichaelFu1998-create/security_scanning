def iterparse(filelike, encoding=None, handler_class=DrillHandler, xpath=None):
    """
    :param filelike: A file-like object with a ``read`` method
    :returns: An iterator yielding :class:`XmlElement` objects
    """
    parser = expat.ParserCreate(encoding)
    elem_iter = DrillElementIterator(filelike, parser)
    handler = handler_class(elem_iter, xpath)
    parser.buffer_text = 1
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.characters
    return elem_iter