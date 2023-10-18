def increment(itr, n=1, format_msg="{}. "):
    """Similar to enumerate but will set format_msg.format(n) into the prefix on
    each iteration

    :Example:
        for v in increment(["foo", "bar"]):
            echo.out(v) # 1. foo\n2. bar

    :param itr: iterator, any iterator you want to set a numeric prefix on on every
        iteration
    :param n: integer, the starting integer for the numeric prefix
    :param format_msg: string, this will basically do: format_msg.format(n) so there
        should only be one set of curly brackets
    :returns: yield generator
    """
    for i, v in enumerate(itr, n):
        with prefix(format_msg, i):
            yield v