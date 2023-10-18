def autoconvert(s):
    """Convert input to a numerical type if possible.

    1. A non-string object is returned as it is
    2. Try conversion to int, float, str.
    """
    if type(s) is not str:
        return s
    for converter in int, float, str:   # try them in increasing order of lenience
        try:
            s = [converter(i) for i in s.split()]
            if len(s) == 1:
                return s[0]
            else:
                return numpy.array(s)
        except (ValueError, AttributeError):
            pass
    raise ValueError("Failed to autoconvert {0!r}".format(s))