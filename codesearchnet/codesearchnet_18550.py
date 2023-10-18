def pack(prev, n, rest=False, **kw):
    """pack pipe takes n elements from previous generator and yield one
    list to next.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param rest: Set True to allow to output the rest part of last elements.
    :type prev: boolean
    :param padding: Specify the padding element for the rest part of last elements.
    :type prev: boolean
    :returns: generator

    :Example:
    >>> result([1,2,3,4,5,6,7] | pack(3))
    [[1, 2, 3], [4, 5, 6]]

    >>> result([1,2,3,4,5,6,7] | pack(3, rest=True))
    [[1, 2, 3], [4, 5, 6], [7,]]

    >>> result([1,2,3,4,5,6,7] | pack(3, padding=None))
    [[1, 2, 3], [4, 5, 6], [7, None, None]]
    """

    if 'padding' in kw:
        use_padding = True
        padding = kw['padding']
    else:
        use_padding = False
        padding = None

    items = []
    for i, data in enumerate(prev, 1):
        items.append(data)
        if (i % n) == 0:
            yield items
            items = []
    if len(items) != 0 and rest:
        if use_padding:
            items.extend([padding, ] * (n - (i % n)))
        yield items