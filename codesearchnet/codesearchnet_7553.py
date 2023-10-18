def _twosided_zerolag(data, zerolag):
    """Build a symmetric vector out of stricly positive lag vector and zero-lag

    .. doctest::

        >>> data = [3,2,1]
        >>> zerolag = 4
        >>> twosided_zerolag(data, zerolag)
        array([1, 2, 3, 4, 3, 2, 1])

    .. seealso:: Same behaviour as :func:`twosided_zerolag`
    """
    res = twosided(np.insert(data, 0, zerolag))
    return res