def window_nuttall(N):
    r"""Nuttall tapering window

    :param N: window length

    .. math:: w(n) = a_0 - a_1 \cos\left(\frac{2\pi n}{N-1}\right)+ a_2 \cos\left(\frac{4\pi n}{N-1}\right)- a_3 \cos\left(\frac{6\pi n}{N-1}\right)

    with :math:`a_0 = 0.355768`, :math:`a_1 = 0.487396`, :math:`a_2=0.144232` and :math:`a_3=0.012604`

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'nuttall', mindB=-80)


    .. seealso:: :func:`create_window`, :class:`Window`
    """
    a0 = 0.355768
    a1 = 0.487396
    a2 = 0.144232
    a3 = 0.012604

    return _coeff4(N, a0, a1, a2, a3)