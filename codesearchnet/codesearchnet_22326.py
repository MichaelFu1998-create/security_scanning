def Text(value, encoding=None):
    """
    Parse a value as text.

    :type  value: `unicode` or `bytes`
    :param value: Text value to parse

    :type  encoding: `bytes`
    :param encoding: Encoding to treat ``bytes`` values as, defaults to
        ``utf-8``.

    :rtype: `unicode`
    :return: Parsed text or ``None`` if ``value`` is neither `bytes` nor
        `unicode`.
    """
    if encoding is None:
        encoding = 'utf-8'
    if isinstance(value, bytes):
        return value.decode(encoding)
    elif isinstance(value, unicode):
        return value
    return None