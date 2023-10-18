def window_blackman_harris(N):
    r"""Blackman Harris window

    :param N: window length

    .. math:: w(n) = a_0 - a_1 \cos\left(\frac{2\pi n}{N-1}\right)+ a_2 \cos\left(\frac{4\pi n}{N-1}\right)- a_3 \cos\left(\frac{6\pi n}{N-1}\right)

    =============== =========
    coeff            value
    =============== =========
    :math:`a_0`     0.35875
    :math:`a_1`     0.48829
    :math:`a_2`     0.14128
    :math:`a_3`     0.01168
    =============== =========

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'blackman_harris', mindB=-80)

    .. seealso:: :func:`spectrum.window.create_window`
    .. seealso:: :func:`create_window`, :class:`Window`
    """
    a0 = 0.35875
    a1 = 0.48829
    a2 = 0.14128
    a3 = 0.01168
    return _coeff4(N, a0, a1, a2, a3)