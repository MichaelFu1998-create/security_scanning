def window_riemann(N):
    r"""Riemann tapering window

    :param int N: window length

    .. math:: w(n) = 1 - \left| \frac{n}{N/2}  \right|^2

    with :math:`-N/2 \leq n \leq N/2`.

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'riesz')

    .. seealso:: :func:`create_window`, :class:`Window`
    """
    n = linspace(-N/2., (N)/2., N)
    w = sin(n/float(N)*2.*pi) / (n / float(N)*2.*pi)
    return w