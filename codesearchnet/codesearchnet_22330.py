def Timestamp(value, _divisor=1., tz=UTC, encoding=None):
    """
    Parse a value as a POSIX timestamp in seconds.

    :type  value: `unicode` or `bytes`
    :param value: Text value to parse, which should be the number of seconds
        since the epoch.

    :type  _divisor: `float`
    :param _divisor: Number to divide the value by.

    :type  tz: `tzinfo`
    :param tz: Timezone, defaults to UTC.

    :type  encoding: `bytes`
    :param encoding: Encoding to treat `bytes` values as, defaults to
        ``utf-8``.

    :rtype: `datetime.datetime`
    :return: Parsed datetime or ``None`` if ``value`` could not be parsed.
    """
    value = Float(value, encoding)
    if value is not None:
        value = value / _divisor
        return datetime.fromtimestamp(value, tz)
    return None