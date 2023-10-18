def batchstack(size, iterable=None, rest=False):
    """
    todo : add example
    :param size:
    :param iterable:
    :param rest:
    :return:
    """

    def stack(data):
        import numpy as np
        return map(np.vstack, data)

    fn = batchzip(size, rest=rest) >> flow(stack)

    return fn if iterable is None else fn(iterable)