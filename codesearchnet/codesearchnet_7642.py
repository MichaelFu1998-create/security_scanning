def window_poisson_hanning(N, alpha=2):
    r"""Hann-Poisson tapering window

    This window is constructed as the product of the Hanning and Poisson
    windows. The parameter **alpha** is the Poisson parameter.

    :param int N: window length
    :param float alpha: parameter of the poisson window

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'poisson_hanning', alpha=0.5)
        window_visu(64, 'poisson_hanning', alpha=1)
        window_visu(64, 'poisson_hanning')

    .. seealso:: :func:`window_poisson`, :func:`window_hann`
    """
    w1 = window_hann(N)
    w2 = window_poisson(N, alpha=alpha)
    return w1*w2