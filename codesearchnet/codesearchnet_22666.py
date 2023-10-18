def arktimestamp(arkt, forfilename=False):
    """Returns a human-readable timestamp given an Ark timestamp 'arct'.
    An Ark timestamp is the number of seconds since Genesis block,
    2017:03:21 15:55:44."""

    t = arkt + time.mktime((2017, 3, 21, 15, 55, 44, 0, 0, 0))
    return '%d %s' % (arkt, timestamp(t))