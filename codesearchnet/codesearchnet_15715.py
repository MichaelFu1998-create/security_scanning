def full_like(array, value, dtype=None):
    """ Create a shared memory array with the same shape and type as a given array, filled with `value`.
    """
    shared = empty_like(array, dtype)
    shared[:] = value
    return shared