def to_color(c):
    """Try to coerce the argument into a color - a 3-tuple of numbers-"""
    if isinstance(c, numbers.Number):
        return c, c, c

    if not c:
        raise ValueError('Cannot create color from empty "%s"' % c)

    if isinstance(c, str):
        return name_to_color(c)

    if isinstance(c, list):
        c = tuple(c)

    if isinstance(c, tuple):
        if len(c) > 3:
            return c[:3]
        while len(c) < 3:
            c += (c[-1],)
        return c

    raise ValueError('Cannot create color from "%s"' % c)