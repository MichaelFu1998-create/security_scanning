def data_cosine(N=1024, A=0.1, sampling=1024., freq=200):
    r"""Return a noisy cosine at a given frequency.

    :param N:           the final data size
    :param A:           the strength of the noise
    :param float sampling: sampling frequency of the input :attr:`data`.
    :param float freq:  the frequency :math:`f_0` of the cosine.

    .. math:: x[t] = cos(2\pi t * f_0) + A w[t]

    where w[t] is a white noise of variance 1.

    .. doctest::

        >>> from spectrum import data_cosine
        >>> a = data_cosine(N=1024, sampling=1024, A=0.5, freq=100)

    """
    t = arange(0, float(N)/sampling, 1./sampling)
    x = cos(2.*pi*t*freq) + A * randn(t.size)
    return x