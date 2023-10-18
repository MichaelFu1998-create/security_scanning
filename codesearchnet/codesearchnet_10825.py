def sqrt_rc_imp(Ns,alpha,M=6):
    """
    A truncated square root raised cosine pulse used in digital communications.

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

    Notes
    -----
    The pulse shape b is typically used as the FIR filter coefficients
    when forming a pulse shaped digital communications waveform. When 
    square root raised cosine (SRC) pulse is used to generate Tx signals and
    at the receiver used as a matched filter (receiver FIR filter), the 
    received signal is now raised cosine shaped, thus having zero
    intersymbol interference and the optimum removal of additive white 
    noise if present at the receiver input.

    Examples
    --------
    Ten samples per symbol and :math:`\\alpha = 0.35`.

    >>> import matplotlib.pyplot as plt
    >>> from numpy import arange
    >>> from sk_dsp_comm.digitalcom import sqrt_rc_imp
    >>> b = sqrt_rc_imp(10,0.35)
    >>> n = arange(-10*6,10*6+1)
    >>> plt.stem(n,b)
    >>> plt.show()
    """
    # Design the filter
    n = np.arange(-M*Ns,M*Ns+1)
    b = np.zeros(len(n))
    Ns *= 1.0
    a = alpha
    for i in range(len(n)):
       if abs(1 - 16*a**2*(n[i]/Ns)**2) <= np.finfo(np.float).eps/2:
           b[i] = 1/2.*((1+a)*np.sin((1+a)*np.pi/(4.*a))-(1-a)*np.cos((1-a)*np.pi/(4.*a))+(4*a)/np.pi*np.sin((1-a)*np.pi/(4.*a)))
       else:
           b[i] = 4*a/(np.pi*(1 - 16*a**2*(n[i]/Ns)**2))
           b[i] = b[i]*(np.cos((1+a)*np.pi*n[i]/Ns) + np.sinc((1-a)*n[i]/Ns)*(1-a)*np.pi/(4.*a))
    return b