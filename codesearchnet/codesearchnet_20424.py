def loads(s, separator=DEFAULT, index_separator=DEFAULT, cls=dict, list_cls=list):
    '''Loads an object from a string.

    :param s: An object to parse
    :type s: bytes or str
    :param separator: The separator between key and value.  Defaults to u'|' or b'|', depending on the types.
    :param index_separator: The separator between key and index.  Defaults to u'_' or b'_', depending on the types.
    :param cls: A callable that returns a Mapping that is filled with pairs.  The most common alternate option would be OrderedDict.
    :param list_cls: A callable that takes an iterable and returns a sequence.
    '''

    if isinstance(s, six.text_type):
        io = StringIO(s)
    else:
        io = BytesIO(s)

    return load(
        fp=io,
        separator=separator,
        index_separator=index_separator,
        cls=cls,
        list_cls=list_cls,
        )