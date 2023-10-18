def diff(iterable):
    """Diff elements of a sequence:
    s -> s0 - s1, s1 - s2, s2 - s3, ...
    """
    a, b = tee(iterable)
    next(b, None)
    return (i - j for i, j in izip(a, b))