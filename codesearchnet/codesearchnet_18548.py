def flatten(prev, depth=sys.maxsize):
    """flatten pipe extracts nested item from previous pipe.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param depth: The deepest nested level to be extracted. 0 means no extraction.
    :type depth: integer
    :returns: generator
    """
    def inner_flatten(iterable, curr_level, max_levels):
        for i in iterable:
            if hasattr(i, '__iter__') and curr_level < max_levels:
                for j in inner_flatten(i, curr_level + 1, max_levels):
                    yield j
            else:
                yield i

    for d in prev:
        if hasattr(d, '__iter__') and depth > 0:
            for inner_d in inner_flatten(d, 1, depth):
                yield inner_d
        else:
            yield d