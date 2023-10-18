def translate(s, table, deletions=""):
    """translate(s,table [,deletions]) -> string

    Return a copy of the string s, where all characters occurring
    in the optional argument deletions are removed, and the
    remaining characters have been mapped through the given
    translation table, which must be a string of length 256.  The
    deletions argument is not allowed for Unicode strings.

    """
    if deletions or table is None:
        return s.translate(table, deletions)
    else:
        # Add s[:0] so that if s is Unicode and table is an 8-bit string,
        # table is converted to Unicode.  This means that table *cannot*
        # be a dictionary -- for that feature, use u.translate() directly.
        return s.translate(table + s[:0])