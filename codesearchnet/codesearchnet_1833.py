def findall(pattern, string, flags=0):
    """Return a list of all non-overlapping matches in the string.

    If one or more groups are present in the pattern, return a
    list of groups; this will be a list of tuples if the pattern
    has more than one group.

    Empty matches are included in the result."""
    return _compile(pattern, flags).findall(string)

    # if sys.hexversion >= 0x02020000:
    #     __all__.append("finditer")
    def finditer(pattern, string, flags=0):
        """Return an iterator over all non-overlapping matches in the
        string.  For each match, the iterator returns a match object.

        Empty matches are included in the result."""
        return _compile(pattern, flags).finditer(string)