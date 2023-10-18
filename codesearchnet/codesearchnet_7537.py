def morlet(lb, ub, n):
    r"""Generate the Morlet waveform


    The Morlet waveform is defined as follows:

    .. math:: w[x] = \cos{5x}  \exp^{-x^2/2}

    :param lb: lower bound
    :param ub: upper bound
    :param int n: waveform data samples


    .. plot::
        :include-source:
        :width: 80%

        from spectrum import morlet
        from pylab import plot
        plot(morlet(0,10,100))

    """
    if n <= 0:
        raise ValueError("n must be strictly positive")

    x = numpy.linspace(lb, ub, n)
    psi = numpy.cos(5*x) * numpy.exp(-x**2/2.)
    return psi