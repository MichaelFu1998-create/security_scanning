def rc_imp(Ns,alpha,M=6):
    """
    A truncated raised cosine pulse used in digital communications.

    The pulse shaping factor :math:`0 < \\alpha < 1` is required as well as the
    truncation factor M which sets the pulse duration to be :math:`2*M*T_{symbol}`.

    Parameters
    ----------
    Ns : number of samples per symbol
    alpha : excess bandwidth factor on (0, 1), e.g., 0.35
    M : equals RC one-sided symbol truncation factor

    Returns
    -------
    b : ndarray containing the pulse shape

    See Also
    --------
    sqrt_rc_imp

    Notes
    -----
    The pulse shape b is typically used as the FIR filter coefficients
    when forming a pulse shaped digital communications waveform.

    Examples
    --------
    Ten samples per symbol and :math:`\\alpha = 0.35`.

    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm.digitalcom import rc_imp
    >>> from numpy import arange
    >>> b = rc_imp(10,0.35)
    >>> n = arange(-10*6,10*6+1)
    >>> plt.stem(n,b)
    >>> plt.show()
    """
    # Design the filter
    n = np.arange(-M*Ns,M*Ns+1)
    b = np.zeros(len(n))
    a = alpha
    Ns *= 1.0
    for i in range(len(n)):
        if (1 - 4*(a*n[i]/Ns)**2) == 0:
            b[i] = np.pi/4*np.sinc(1/(2.*a))
        else:
            b[i] = np.sinc(n[i]/Ns)*np.cos(np.pi*a*n[i]/Ns)/(1 - 4*(a*n[i]/Ns)**2)
    return b