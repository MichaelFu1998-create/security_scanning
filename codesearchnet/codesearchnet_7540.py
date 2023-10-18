def ac2poly(data):
    """Convert autocorrelation sequence to prediction polynomial

    :param array data:    input data (list or numpy.array)
    :return:
        * AR parameters
        * noise variance

    This is an alias to::

        a, e, c = LEVINSON(data)

    :Example:

    .. doctest::

        >>> from spectrum import ac2poly
        >>> from numpy import array
        >>> r = [5, -2, 1.01]
        >>> ar, e = ac2poly(r)
        >>> ar
        array([ 1.  ,  0.38, -0.05])
        >>> e
        4.1895000000000007

    """
    a, e, _c = LEVINSON(data)
    a = numpy.insert(a, 0, 1)
    return a, e