def Delimited(value, parser=Text, delimiter=u',', encoding=None):
    """
    Parse a value as a delimited list.

    :type  value: `unicode` or `bytes`
    :param value: Text value to parse.

    :type  parser: `callable` taking a `unicode` parameter
    :param parser: Callable to map over the delimited text values.

    :type  delimiter: `unicode`
    :param delimiter: Delimiter text.

    :type  encoding: `bytes`
    :param encoding: Encoding to treat `bytes` values as, defaults to
        ``utf-8``.

    :rtype: `list`
    :return: List of parsed values.
    """
    value = Text(value, encoding)
    if value is None or value == u'':
        return []
    return map(parser, value.split(delimiter))