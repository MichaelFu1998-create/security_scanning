def window_blackman(N, alpha=0.16):
    r"""Blackman window

    :param N: window length

    .. math:: a_0 - a_1 \cos(\frac{2\pi n}{N-1}) +a_2 \cos(\frac{4\pi n }{N-1})

    with

    .. math::

        a_0 = (1-\alpha)/2, a_1=0.5, a_2=\alpha/2 \rm{\;and\; \alpha}=0.16

    When :math:`\alpha=0.16`, this is the unqualified Blackman window with
    :math:`a_0=0.48`  and :math:`a_2=0.08`.

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'blackman')

    .. note:: Although Numpy implements a blackman window for :math:`\alpha=0.16`,
        this implementation is valid for any :math:`\alpha`.

    .. seealso:: numpy.blackman, :func:`create_window`, :class:`Window`

    """
    a0 = (1. - alpha)/2.
    a1 = 0.5
    a2 = alpha/2.

    if (N == 1):
        win = array([1.])
    else:
        k = arange(0, N)/float(N-1.)
        win =  a0 - a1 * cos (2 * pi * k) + a2 * cos (4 * pi * k)
    return win