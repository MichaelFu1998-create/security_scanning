def ibatch(size, iterable=None, rest=False):
    """
    add example
    :param size:
    :param iterable:
    :param rest:
    :return:
    """

    @iterflow
    def exact_size(it):
        it = iter(it)
        while True:
            yield [it.next() for _ in xrange(size)]

    @iterflow
    def at_most(it):
        it = iter(it)
        while True:
            data = []
            for _ in xrange(size):
                try:
                    data.append(it.next())
                except StopIteration:
                    if data:
                        yield data
                    raise StopIteration
            yield data

    ibatchit = at_most if rest else exact_size

    return ibatchit if iterable is None else ibatchit(iterable)