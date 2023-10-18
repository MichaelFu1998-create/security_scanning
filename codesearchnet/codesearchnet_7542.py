def rc2ac(k, R0):
    """Convert reflection coefficients to autocorrelation sequence.

    :param k: reflection coefficients
    :param R0: zero-lag autocorrelation
    :returns: the autocorrelation sequence

    .. seealso:: :func:`ac2rc`, :func:`poly2rc`, :func:`ac2poly`, :func:`poly2rc`, :func:`rc2poly`.

    """
    [a,efinal] = rc2poly(k, R0)
    R, u, kr, e = rlevinson(a, efinal)
    return R