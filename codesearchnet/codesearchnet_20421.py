def dump(obj, fp, startindex=1, separator=DEFAULT, index_separator=DEFAULT):
    '''Dump an object in req format to the fp given.

    :param Mapping obj: The object to serialize.  Must have a keys method.
    :param fp: A writable that can accept all the types given.
    :param separator: The separator between key and value.  Defaults to u'|' or b'|', depending on the types.
    :param index_separator: The separator between key and index.  Defaults to u'_' or b'_', depending on the types.
    '''

    if startindex < 0:
        raise ValueError('startindex must be non-negative, but was {}'.format(startindex))

    try:
        firstkey = next(iter(obj.keys()))
    except StopIteration:
        return

    if isinstance(firstkey, six.text_type):
        converter = six.u
    else:
        converter = six.b

    default_separator = converter('|')
    default_index_separator = converter('_')
    newline = converter('\n')

    if separator is DEFAULT:
        separator = default_separator
    if index_separator is DEFAULT:
        index_separator = default_index_separator

    for key, value in six.iteritems(obj):
        if isinstance(value, (list, tuple, set)):
            for index, item in enumerate(value, start=startindex):
                fp.write(key)
                fp.write(index_separator)
                fp.write(converter(str(index)))
                fp.write(separator)
                fp.write(item)
                fp.write(newline)
        else:
            fp.write(key)
            fp.write(separator)
            fp.write(value)
            fp.write(newline)