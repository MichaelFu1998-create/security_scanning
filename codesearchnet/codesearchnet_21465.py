def parse(url_or_path, encoding=None, handler_class=DrillHandler):
    """
    :param url_or_path: A file-like object, a filesystem path, a URL, or a string containing XML
    :rtype: :class:`XmlElement`
    """
    handler = handler_class()
    parser = expat.ParserCreate(encoding)
    parser.buffer_text = 1
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.characters
    if isinstance(url_or_path, basestring):
        if '://' in url_or_path[:20]:
            with contextlib.closing(url_lib.urlopen(url_or_path)) as f:
                parser.ParseFile(f)
        elif url_or_path[:100].strip().startswith('<'):
            if isinstance(url_or_path, unicode):
                if encoding is None:
                    encoding = 'utf-8'
                url_or_path = url_or_path.encode(encoding)
            parser.Parse(url_or_path, True)
        else:
            with open(url_or_path, 'rb') as f:
                parser.ParseFile(f)
    elif PY3 and isinstance(url_or_path, bytes):
        parser.ParseFile(bytes_io(url_or_path))
    else:
        parser.ParseFile(url_or_path)
    return handler.root