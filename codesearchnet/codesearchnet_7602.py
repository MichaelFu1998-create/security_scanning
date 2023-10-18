def arma2psd(A=None, B=None, rho=1., T=1., NFFT=4096, sides='default',
        norm=False):
    r"""Computes power spectral density given ARMA values.

    This function computes the power spectral density values
    given the ARMA parameters of an ARMA model. It assumes that
    the driving sequence is a white noise process of zero mean and
    variance :math:`\rho_w`. The sampling frequency and noise variance are
    used to scale the PSD output, which length is set by the user with the
    `NFFT` parameter.

    :param array A:   Array of AR parameters (complex or real)
    :param array B:   Array of MA parameters (complex or real)
    :param float rho: White noise variance to scale the returned PSD
    :param float T:   Sample interval in seconds to scale the returned PSD
    :param int NFFT:  Final size of the PSD
    :param str sides: Default PSD is two-sided, but sides can be set to centerdc.

    .. warning:: By convention, the AR or MA arrays does not contain the
        A0=1 value.

    If :attr:`B` is None, the model is a pure AR model. If :attr:`A` is None,
    the model is a pure MA model.

    :return: two-sided PSD

    .. rubric:: Details:

    AR case: the power spectral density is:

    .. math:: P_{ARMA}(f) = T \rho_w \left|\frac{B(f)}{A(f)}\right|^2

    where:

    .. math:: A(f) = 1 + \sum_{k=1}^q b(k) e^{-j2\pi fkT}
    .. math:: B(f) = 1 + \sum_{k=1}^p a(k) e^{-j2\pi fkT}

    .. rubric:: **Example:**

    .. plot::
        :width: 80%
        :include-source:

        import spectrum.arma
        from pylab import plot, log10, legend
        plot(10*log10(spectrum.arma.arma2psd([1,0.5],[0.5,0.5])), label='ARMA(2,2)')
        plot(10*log10(spectrum.arma.arma2psd([1,0.5],None)), label='AR(2)')
        plot(10*log10(spectrum.arma.arma2psd(None,[0.5,0.5])), label='MA(2)')
        legend()

    :References: [Marple]_
    """
    if NFFT is None:
        NFFT = 4096

    if A is None and B is None:
        raise ValueError("Either AR or MA model must be provided")

    psd = np.zeros(NFFT, dtype=complex)

    if A is not None:
        ip = len(A)
        den = np.zeros(NFFT, dtype=complex)
        den[0] = 1.+0j
        for k in range(0, ip):
            den[k+1] = A[k]
        denf = fft(den, NFFT)

    if B is not None:
        iq = len(B)
        num = np.zeros(NFFT, dtype=complex)
        num[0] = 1.+0j
        for k in range(0, iq):
            num[k+1] = B[k]
        numf = fft(num, NFFT)

    # Changed in version 0.6.9 (divided by T instead of multiply)
    if A is not None and B is not None:
        psd = rho / T * abs(numf)**2. / abs(denf)**2.
    elif A is not None:
        psd = rho / T / abs(denf)**2.
    elif B is not None:
        psd = rho / T * abs(numf)**2.


    psd = np.real(psd)
    # The PSD is a twosided PSD.
    # to obtain the centerdc
    if sides != 'default':
        from . import tools
        assert sides in ['centerdc']
        if sides == 'centerdc':
            psd = tools.twosided_2_centerdc(psd)

    if norm == True:
        psd /= max(psd)

    return psd