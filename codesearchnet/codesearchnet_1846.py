def _count_leading(line, ch):
    """
    Return number of `ch` characters at the start of `line`.

    Example:

    >>> _count_leading('   abc', ' ')
    3
    """

    i, n = 0, len(line)
    while i < n and line[i] == ch:
        i += 1
    return i