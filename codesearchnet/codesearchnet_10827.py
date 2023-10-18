def my_psd(x,NFFT=2**10,Fs=1):
    """
    A local version of NumPy's PSD function that returns the plot arrays.

    A mlab.psd wrapper function that returns two ndarrays;
    makes no attempt to auto plot anything.

    Parameters
    ----------
    x : ndarray input signal
    NFFT : a power of two, e.g., 2**10 = 1024
    Fs : the sampling rate in Hz

    Returns
    -------
    Px : ndarray of the power spectrum estimate
    f : ndarray of frequency values
    
    Notes
    -----
    This function makes it easier to overlay spectrum plots because
    you have better control over the axis scaling than when using psd()
    in the autoscale mode.
    
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import digitalcom as dc
    >>> from numpy import log10
    >>> x,b, data = dc.NRZ_bits(10000,10)
    >>> Px,f = dc.my_psd(x,2**10,10)
    >>> plt.plot(f, 10*log10(Px))
    >>> plt.show()
    """
    Px,f = pylab.mlab.psd(x,NFFT,Fs)
    return Px.flatten(), f