def batches(iterable, n=1):
    """
    From http://stackoverflow.com/a/8290508/270334
    :param n:
    :param iterable:
    """
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]