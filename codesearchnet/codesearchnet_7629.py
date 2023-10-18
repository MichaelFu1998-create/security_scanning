def window_bartlett_hann(N):
    r"""Bartlett-Hann window

    :param N: window length

    .. math:: w(n) = a_0 + a_1 \left| \frac{n}{N-1} -\frac{1}{2}\right| - a_2 \cos \left( \frac{2\pi n}{N-1} \right)

    with :math:`a_0 = 0.62`, :math:`a_1 = 0.48` and :math:`a_2=0.38`

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'bartlett_hann')

    .. seealso:: :func:`create_window`, :class:`Window`
    """
    if N == 1:
        return ones(1)
    n = arange(0, N)

    a0 = 0.62
    a1 = 0.48
    a2 = 0.38

    win = a0 -  a1 *abs(n/(N-1.)-0.5) -a2 * cos(2*pi*n/(N-1.))
    return win