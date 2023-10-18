def _frange(start, stop=None, step=None):
    """
    _frange range like function for float inputs
    :param start:
    :type start:
    :param stop:
    :type stop:
    :param step:
    :type step:
    :return:
    :rtype:
    """
    if stop is None:
        stop = start
        start = 0.0
    if step is None:
        step = 1.0
    r = start
    while r < stop:
        yield r
        r += step