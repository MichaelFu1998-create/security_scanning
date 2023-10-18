def _normalize(c):
    """
    Convert a byte-like value into a canonical byte (a value of type 'bytes' of len 1)

    :param c:
    :return:
    """
    if isinstance(c, int):
        return bytes([c])
    elif isinstance(c, str):
        return bytes([ord(c)])
    else:
        return c