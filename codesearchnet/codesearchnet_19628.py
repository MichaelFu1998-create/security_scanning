def shuffle(qsize=1024, iterable=None):
    """
    add example
    :param qsize:
    :param iterable:
    :return:
    """

    @iterflow
    def shuffleit(it):
        from random import randrange
        q = []

        for i, d in enumerate(it):
            q.insert(randrange(0, len(q) + 1), d)
            if i < qsize:
                continue
            yield q.pop(randrange(0, len(q)))

        while q:
            yield q.pop(randrange(0, len(q)))

    return shuffleit if iterable is None else shuffleit(iterable)