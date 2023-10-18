def window_gaussian(N, alpha=2.5):
    r"""Gaussian window

    :param N: window length

    .. math:: \exp^{-0.5 \left( \sigma\frac{n}{N/2} \right)^2}

    with :math:`\frac{N-1}{2}\leq n \leq \frac{N-1}{2}`.

    .. note:: N-1 is used to be in agreement with octave convention. The ENBW of
         1.4 is also in agreement with [Harris]_

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'gaussian', alpha=2.5)



    .. seealso:: scipy.signal.gaussian, :func:`create_window`
    """
    t = linspace(-(N-1)/2., (N-1)/2., N)
    #t = linspace(-(N)/2., (N)/2., N)
    w = exp(-0.5*(alpha * t/(N/2.))**2.)
    return w