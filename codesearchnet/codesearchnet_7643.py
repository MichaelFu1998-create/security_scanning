def window_cauchy(N, alpha=3):
    r"""Cauchy tapering window

    :param int N: window length
    :param float alpha: parameter of the poisson window

    .. math:: w(n) = \frac{1}{1+\left(\frac{\alpha*n}{N/2}\right)**2}

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'cauchy', alpha=3)
        window_visu(64, 'cauchy', alpha=4)
        window_visu(64, 'cauchy', alpha=5)


    .. seealso:: :func:`window_poisson`, :func:`window_hann`
    """
    n = linspace(-N/2., (N)/2., N)
    w = 1./(1.+ (alpha*n/(N/2.))**2)
    return w