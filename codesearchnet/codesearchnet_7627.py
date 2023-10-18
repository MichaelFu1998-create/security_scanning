def window_cosine(N):
    r"""Cosine tapering window also known as sine window.

    :param N: window length

    .. math:: w(n) = \cos\left(\frac{\pi n}{N-1} - \frac{\pi}{2}\right) = \sin \left(\frac{\pi n}{N-1}\right)

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'cosine')

    .. seealso:: :func:`create_window`, :class:`Window`
    """
    if N ==1:
        return ones(1)
    n = arange(0, N)
    win = sin(pi*n/(N-1.))
    return win