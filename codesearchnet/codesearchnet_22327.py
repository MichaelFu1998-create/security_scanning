def Integer(value, base=10, encoding=None):
    """
    Parse a value as an integer.

    :type  value: `unicode` or `bytes`
    :param value: Text value to parse

    :type  base: `unicode` or `bytes`
    :param base: Base to assume ``value`` is specified in.

    :type  encoding: `bytes`
    :param encoding: Encoding to treat ``bytes`` values as, defaults to
        ``utf-8``.

    :rtype: `int`
    :return: Parsed integer or ``None`` if ``value`` could not be parsed as an
        integer.
    """
    try:
        return int(Text(value, encoding), base)
    except (TypeError, ValueError):
        return None