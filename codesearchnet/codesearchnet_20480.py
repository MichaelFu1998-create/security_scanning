def smart_str(value, encoding='utf-8', errors='strict'):
    """Convert Python object to string.

    :param value: Python object to convert.
    :param encoding: Encoding to use if in Python 2 given object is unicode.
    :param errors: Errors mode to use if in Python 2 given object is unicode.
    """
    if not IS_PY3 and isinstance(value, unicode):  # noqa
        return value.encode(encoding, errors)
    return str(value)