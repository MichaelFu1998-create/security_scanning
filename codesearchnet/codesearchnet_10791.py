def peaking(GdB, fc, Q=3.5, fs=44100.):
    """
    A second-order peaking filter having GdB gain at fc and approximately
    and 0 dB otherwise.
    
    The filter coefficients returns correspond to a biquadratic system function
    containing five parameters.
    
    Parameters
    ----------
    GdB : Lowpass gain in dB
    fc : Center frequency in Hz
    Q : Filter Q which is inversely proportional to bandwidth
    fs : Sampling frquency in Hz
    
    Returns
    -------
    b : ndarray containing the numerator filter coefficients
    a : ndarray containing the denominator filter coefficients
    
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> from sk_dsp_comm.sigsys import peaking
    >>> from scipy import signal
    >>> b,a = peaking(2.0,500)
    >>> f = np.logspace(1,5,400)
    >>> w,H = signal.freqz(b,a,2*np.pi*f/44100)
    >>> plt.semilogx(f,20*np.log10(abs(H)))
    >>> plt.ylabel("Power Spectral Density (dB)")
    >>> plt.xlabel("Frequency (Hz)")
    >>> plt.show()

    >>> b,a = peaking(-5.0,500,4)
    >>> w,H = signal.freqz(b,a,2*np.pi*f/44100)
    >>> plt.semilogx(f,20*np.log10(abs(H)))
    >>> plt.ylabel("Power Spectral Density (dB)")
    >>> plt.xlabel("Frequency (Hz)")
    """
    mu = 10**(GdB/20.)
    kq = 4/(1 + mu)*np.tan(2*np.pi*fc/fs/(2*Q))
    Cpk = (1 + kq *mu)/(1 + kq)
    b1 = -2*np.cos(2*np.pi*fc/fs)/(1 + kq*mu)
    b2 = (1 - kq*mu)/(1 + kq*mu)
    a1 = -2*np.cos(2*np.pi*fc/fs)/(1 + kq)
    a2 = (1 - kq)/(1 + kq)
    b = Cpk*np.array([1, b1, b2])
    a = np.array([1, a1, a2])
    return b,a