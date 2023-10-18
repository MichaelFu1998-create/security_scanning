def save_split(s, sep, maxsplit):
    """Split string, always returning n-tuple (filled with None if necessary)."""
    tok = s.split(sep, maxsplit)
    while len(tok) <= maxsplit:
        tok.append(None)
    return tok