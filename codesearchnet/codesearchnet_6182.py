def string_repr(s):
    """Return a string as hex dump."""
    if compat.is_bytes(s):
        res = "{!r}: ".format(s)
        for b in s:
            if type(b) is str:  # Py2
                b = ord(b)
            res += "%02x " % b
        return res
    return "{}".format(s)