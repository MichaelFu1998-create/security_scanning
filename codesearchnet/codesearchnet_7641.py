def window_poisson(N, alpha=2):
    r"""Poisson tapering window

    :param int N: window length

    .. math:: w(n) = \exp^{-\alpha \frac{|n|}{N/2} }

    with :math:`-N/2 \leq n \leq N/2`.

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'poisson')
        window_visu(64, 'poisson', alpha=3)
        window_visu(64, 'poisson', alpha=4)

    .. seealso:: :func:`create_window`, :class:`Window`
    """
    n = linspace(-N/2., (N)/2., N)
    w = exp(-alpha * abs(n)/(N/2.))
    return w