def threewise(iterable):
    """s -> (None, s0, s1), (s0, s1, s2), ... (sn-1, sn, None)
    example:
    for (last, cur, next) in threewise(l):
    """
    a, b, c = itertools.tee(iterable,3)
    def prepend(val, l):
        yield val
        for i in l: yield i
    def postpend(val, l):
        for i in l: yield i
        yield val
    next(c,None)

    for _xa, _xb, _xc in six.moves.zip(prepend(None,a), b, postpend(None,c)):
        yield (_xa, _xb, _xc)