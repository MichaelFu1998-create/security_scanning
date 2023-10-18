def where_is(strings, pattern, n=1, lookup_func=re.match):
    """Return index of the nth match found of pattern in strings

    Parameters
    ----------
    strings: list of str
        List of strings

    pattern: str
        Pattern to be matched

    nth: int
        Number of times the match must happen to return the item index.

    lookup_func: callable
        Function to match each item in strings to the pattern, e.g., re.match or re.search.

    Returns
    -------
    index: int
        Index of the nth item that matches the pattern.
        If there are no n matches will return -1
    """
    count = 0
    for idx, item in enumerate(strings):
        if lookup_func(pattern, item):
            count += 1
            if count == n:
                return idx
    return -1