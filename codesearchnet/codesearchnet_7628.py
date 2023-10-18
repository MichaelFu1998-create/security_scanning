def window_lanczos(N):
    r"""Lanczos window also known as sinc window.

    :param N: window length

    .. math:: w(n) = sinc \left(  \frac{2n}{N-1} - 1 \right)

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'lanczos')

    .. seealso:: :func:`create_window`, :class:`Window`
    """
    if N ==1:
        return ones(1)

    n = linspace(-N/2., N/2., N)
    win = sinc(2*n/(N-1.))
    return win