def mexican(lb, ub, n):
    r"""Generate the mexican hat wavelet

    The Mexican wavelet is:

    .. math:: w[x] = \cos{5x}  \exp^{-x^2/2}

    :param lb: lower bound
    :param ub: upper bound
    :param int n: waveform data samples
    :return: the waveform

    .. plot::
        :include-source:
        :width: 80%

        from spectrum import mexican
        from pylab import plot
        plot(mexican(0, 10, 100))

    """
    if n <= 0:
        raise ValueError("n must be strictly positive")

    x = numpy.linspace(lb, ub, n)
    psi = (1.-x**2.) * (2./(numpy.sqrt(3.)*pi**0.25)) * numpy.exp(-x**2/2.)
    return psi