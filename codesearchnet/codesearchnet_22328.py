def Boolean(value, true=(u'yes', u'1', u'true'), false=(u'no', u'0', u'false'),
            encoding=None):
    """
    Parse a value as a boolean.

    :type  value: `unicode` or `bytes`
    :param value: Text value to parse.

    :type  true: `tuple` of `unicode`
    :param true: Values to compare, ignoring case, for ``True`` values.

    :type  false: `tuple` of `unicode`
    :param false: Values to compare, ignoring case, for ``False`` values.

    :type  encoding: `bytes`
    :param encoding: Encoding to treat `bytes` values as, defaults to
        ``utf-8``.

    :rtype: `bool`
    :return: Parsed boolean or ``None`` if ``value`` did not match ``true`` or
        ``false`` values.
    """
    value = Text(value, encoding)
    if value is not None:
        value = value.lower().strip()
    if value in true:
        return True
    elif value in false:
        return False
    return None