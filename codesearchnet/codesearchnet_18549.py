def values(prev, *keys, **kw):
    """values pipe extract value from previous pipe.

    If previous pipe send a dictionary to values pipe, keys should contains
    the key of dictionary which you want to get. If previous pipe send list or
    tuple,

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :returns: generator
    """
    d = next(prev)
    if isinstance(d, dict):
        yield [d[k] for k in keys if k in d]
        for d in prev:
            yield [d[k] for k in keys if k in d]
    else:
        yield [d[i] for i in keys if 0 <= i < len(d)]
        for d in prev:
            yield [d[i] for i in keys if 0 <= i < len(d)]