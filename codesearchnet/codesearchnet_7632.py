def window_blackman_nuttall(N):
    r"""Blackman Nuttall window

    returns a minimum, 4-term Blackman-Harris window. The window is minimum in the sense that its maximum sidelobes are minimized.
    The coefficients for this window differ from the Blackman-Harris window coefficients and produce slightly lower sidelobes.

    :param N: window length

    .. math:: w(n) = a_0 - a_1 \cos\left(\frac{2\pi n}{N-1}\right)+ a_2 \cos\left(\frac{4\pi n}{N-1}\right)- a_3 \cos\left(\frac{6\pi n}{N-1}\right)

    with :math:`a_0 = 0.3635819`, :math:`a_1 = 0.4891775`, :math:`a_2=0.1365995` and :math:`0_3=.0106411`

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'blackman_nuttall', mindB=-80)

    .. seealso:: :func:`spectrum.window.create_window`
    .. seealso:: :func:`create_window`, :class:`Window`

    """
    a0 = 0.3635819
    a1 = 0.4891775
    a2 = 0.1365995
    a3 = 0.0106411
    return _coeff4(N, a0, a1, a2, a3)