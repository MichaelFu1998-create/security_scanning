def pascal(n):
    """Return Pascal matrix

    :param int n: size of the matrix

    .. doctest::

        >>> from spectrum import pascal
        >>> pascal(6)
        array([[   1.,    1.,    1.,    1.,    1.,    1.],
               [   1.,    2.,    3.,    4.,    5.,    6.],
               [   1.,    3.,    6.,   10.,   15.,   21.],
               [   1.,    4.,   10.,   20.,   35.,   56.],
               [   1.,    5.,   15.,   35.,   70.,  126.],
               [   1.,    6.,   21.,   56.,  126.,  252.]])

    .. todo:: use the symmetric property to improve computational time if needed
    """
    errors.is_positive_integer(n)
    result = numpy.zeros((n, n))

    #fill the first row and column
    for i in range(0, n):
        result[i, 0] = 1
        result[0, i] = 1
    if n > 1:
        for i in range(1, n):
            for j in range(1, n):
                result[i, j] = result[i-1, j] + result[i, j-1]
    return result