def cshift(data, offset):
    """Circular shift to the right (within an array) by a given offset

    :param array data: input data (list or numpy.array)
    :param int offset: shift the array with the offset

    .. doctest::

        >>> from spectrum import cshift
        >>> cshift([0, 1, 2, 3, -2, -1], 2)
        array([-2, -1,  0,  1,  2,  3])

    """
    # the deque method is suppose to be optimal when using rotate to shift the
    # data that playing with the data to build a new list.
    if isinstance(offset, float):
        offset = int(offset)
    a = deque(data)
    a.rotate(offset)
    return np.array(a)