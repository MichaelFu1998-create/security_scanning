def dumps(obj, startindex=1, separator=DEFAULT, index_separator=DEFAULT):
    '''Dump an object in req format to a string.

    :param Mapping obj: The object to serialize.  Must have a keys method.
    :param separator: The separator between key and value.  Defaults to u'|' or b'|', depending on the types.
    :param index_separator: The separator between key and index.  Defaults to u'_' or b'_', depending on the types.
    '''

    try:
        firstkey = next(iter(obj.keys()))
    except StopIteration:
        return str()

    if isinstance(firstkey, six.text_type):
        io = StringIO()
    else:
        io = BytesIO()

    dump(
        obj=obj,
        fp=io,
        startindex=startindex,
        separator=separator,
        index_separator=index_separator,
        )
    return io.getvalue()