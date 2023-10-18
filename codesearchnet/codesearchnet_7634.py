def window_bohman(N):
    r"""Bohman tapering window

    :param N: window length

    .. math:: w(n) = (1-|x|) \cos (\pi |x|) + \frac{1}{\pi} \sin(\pi |x|)

    where x is a length N vector of linearly spaced values between
    -1 and 1.

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'bohman')

    .. seealso:: :func:`create_window`, :class:`Window`
    """
    x = linspace(-1, 1, N)
    w = (1.-abs(x)) * cos(pi*abs(x)) + 1./pi * sin(pi*abs(x))
    return w