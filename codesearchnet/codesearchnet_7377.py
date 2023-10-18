def parse(s):
    """Regular expression parser

    :param s: Regular expression
    :type s: str
    :rtype: list
    """
    if IS_PY3:
        r = sre_parse.parse(s, flags=U)
    else:
        r = sre_parse.parse(s.decode('utf-8'), flags=U)
    return list(r)