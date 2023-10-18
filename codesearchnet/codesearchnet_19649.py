def chunks(lst, number):
    """
    A generator, split list `lst` into `number` equal size parts.
    usage::

        >>> parts = chunks(range(8),3)
        >>> parts
        <generator object chunks at 0xb73bd964>
        >>> list(parts)
        [[0, 1, 2], [3, 4, 5], [6, 7]]

    """
    lst_len = len(lst)

    for i in xrange(0, lst_len, number):
        yield lst[i: i+number]