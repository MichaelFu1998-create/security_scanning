def window_chebwin(N, attenuation=50):
    """Cheb window

    :param N: window length

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'chebwin', attenuation=50)

    .. seealso:: scipy.signal.chebwin, :func:`create_window`, :class:`Window`
    """
    import scipy.signal
    return scipy.signal.chebwin(N, attenuation)