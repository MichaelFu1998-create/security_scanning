def full(shape, value, dtype='f8'):
    """ Create a shared memory array of given shape and type, filled with `value`.
    """
    shared = empty(shape, dtype)
    shared[:] = value
    return shared