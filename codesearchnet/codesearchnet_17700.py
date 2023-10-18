def minify_hex(_hex):
    """
    Given a HEX value, tries to reduce it from a 6 character hex (e.g. #ffffff) to a 3 character hex (e.g. #fff).
    If the HEX value is unable to be minified, returns the 6 character HEX representation.

    :param _hex:
    :return:
    """
    size = len(_hex.strip('#'))
    if size == 3:
        return _hex
    elif size == 6:
        if _hex[1] == _hex[2] and _hex[3] == _hex[4] and _hex[5] == _hex[6]:
            return _hex[0::2]
        else:
            return _hex
    else:
        raise ColorException('Unexpected HEX size when minifying: {}'.format(size))