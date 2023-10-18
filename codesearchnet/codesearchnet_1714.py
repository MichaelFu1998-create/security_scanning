def needsquoting(c, quotetabs, header):
    """Decide whether a particular character needs to be quoted.

    The 'quotetabs' flag indicates whether embedded tabs and spaces should be
    quoted.  Note that line-ending tabs and spaces are always encoded, as per
    RFC 1521.
    """
    if c in ' \t':
        return quotetabs
    # if header, we have to escape _ because _ is used to escape space
    if c == '_':
        return header
    return c == ESCAPE or not (' ' <= c <= '~')