def _tag_matches_pattern(tag, pattern):
    """Return true if MARC 'tag' matches a 'pattern'.

    'pattern' is plain text, with % as wildcard

    Both parameters must be 3 characters long strings.

    .. doctest::

        >>> _tag_matches_pattern("909", "909")
        True
        >>> _tag_matches_pattern("909", "9%9")
        True
        >>> _tag_matches_pattern("909", "9%8")
        False

    :param tag: a 3 characters long string
    :param pattern: a 3 characters long string
    :return: False or True
    """
    for char1, char2 in zip(tag, pattern):
        if char2 not in ('%', char1):
            return False
    return True