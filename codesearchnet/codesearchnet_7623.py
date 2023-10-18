def window_kaiser(N, beta=8.6, method='numpy'):
    r"""Kaiser window

    :param N: window length
    :param beta: kaiser parameter (default is 8.6)

    To obtain a Kaiser window that designs an FIR filter with
    sidelobe attenuation of :math:`\alpha` dB, use the following :math:`\beta` where
    :math:`\beta = \pi \alpha`.

    .. math::

        w_n = \frac{I_0\left(\pi\alpha\sqrt{1-\left(\frac{2n}{M}-1\right)^2}\right)} {I_0(\pi \alpha)}

    where

      * :math:`I_0` is the zeroth order Modified Bessel function of the first kind.
      * :math:`\alpha` is a real number that determines the shape of the 
        window. It determines the trade-off between main-lobe width and side 
        lobe level.
      * the length of the sequence is N=M+1.

    The Kaiser window can approximate many other windows by varying 
    the :math:`\beta` parameter:

    ===== ========================
    beta  Window shape
    ===== ========================
    0     Rectangular
    5     Similar to a Hamming
    6     Similar to a Hanning
    8.6   Similar to a Blackman
    ===== ========================

    .. plot::
        :width: 80%
        :include-source:

        from pylab import plot, legend, xlim
        from spectrum import window_kaiser
        N = 64
        for beta in [1,2,4,8,16]:
            plot(window_kaiser(N, beta), label='beta='+str(beta))
        xlim(0,N)
        legend()

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'kaiser', beta=8.)

    .. seealso:: numpy.kaiser, :func:`spectrum.window.create_window`
    """
    if N == 1:
        return ones(1)
    if method == 'numpy':
        from numpy import kaiser
        return kaiser(N, beta)
    else:
        return _kaiser(N, beta)