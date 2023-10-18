def scatter(x,Ns,start):
    """
    Sample a baseband digital communications waveform at the symbol spacing.

    Parameters
    ----------
    x : ndarray of the input digital comm signal
    Ns : number of samples per symbol (bit)
    start : the array index to start the sampling

    Returns
    -------
    xI : ndarray of the real part of x following sampling
    xQ : ndarray of the imaginary part of x following sampling

    Notes
    -----
    Normally the signal is complex, so the scatter plot contains 
    clusters at point  in the complex plane. For a binary signal 
    such as BPSK, the point centers are nominally +/-1 on the real
    axis. Start is used to eliminate transients from the FIR
    pulse shaping filters from appearing in the scatter plot.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import digitalcom as dc
    >>> x,b, data = dc.NRZ_bits(1000,10,'rc')

    Add some noise so points are now scattered about +/-1.

    >>> y = dc.cpx_AWGN(x,20,10)
    >>> yI,yQ = dc.scatter(y,10,60)
    >>> plt.plot(yI,yQ,'.')
    >>> plt.grid()
    >>> plt.xlabel('In-Phase')
    >>> plt.ylabel('Quadrature')
    >>> plt.axis('equal')
    >>> plt.show()
    """
    xI = np.real(x[start::Ns])
    xQ = np.imag(x[start::Ns])
    return xI, xQ