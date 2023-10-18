def batchzip(size, iterable=None, rest=False):
    """
    todo : add example
    :param size:
    :param iterable:
    :param rest:
    :return:
    """
    fn = ibatch(size, rest=rest) >> zipflow

    return fn if iterable is None else fn(iterable)