def window_flattop(N, mode='symmetric',precision=None):
    r"""Flat-top tapering window

    Returns symmetric or periodic flat top window.

    :param N: window length
    :param mode: way the data are normalised. If mode is *symmetric*, then
        divide n by N-1. IF mode is *periodic*, divide by N,
        to be consistent with octave code.

    When using windows for filter design, the *symmetric* mode
    should be used (default). When using windows for spectral analysis, the *periodic*
    mode should be used. The mathematical form of the flat-top window in the symmetric
    case is:

    .. math:: w(n) = a_0
        - a_1 \cos\left(\frac{2\pi n}{N-1}\right)
        + a_2 \cos\left(\frac{4\pi n}{N-1}\right)
        - a_3 \cos\left(\frac{6\pi n}{N-1}\right)
        + a_4 \cos\left(\frac{8\pi n}{N-1}\right)

    =====  =============
    coeff  value
    =====  =============
    a0     0.21557895
    a1     0.41663158
    a2     0.277263158
    a3     0.083578947
    a4     0.006947368
    =====  =============

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'bohman')


    .. seealso:: :func:`create_window`, :class:`Window`
    """
    assert mode in ['periodic', 'symmetric']
    t = arange(0, N)

    # FIXME: N=1 for mode = periodic ?
    if mode == 'periodic':
        x = 2*pi*t/float(N)
    else:
        if N ==1:
            return ones(1)
        x = 2*pi*t/float(N-1)
    a0 = 0.21557895
    a1 = 0.41663158
    a2 = 0.277263158
    a3 = 0.083578947
    a4 = 0.006947368

    if precision == 'octave':
        #to compare with octave, same as above but less precise
        d  = 4.6402
        a0 = 1./d
        a1 = 1.93/d
        a2 = 1.29/d
        a3 = 0.388/d
        a4 = 0.0322/d
    w = a0-a1*cos(x)+a2*cos(2*x)-a3*cos(3*x)+a4*cos(4*x)
    return w