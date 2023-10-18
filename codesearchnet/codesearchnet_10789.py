def ten_band_eq_filt(x,GdB,Q=3.5):
    """
    Filter the input signal x with a ten-band equalizer having octave gain values in ndarray GdB.
    
    The signal x is filtered using octave-spaced peaking filters starting at 31.25 Hz and
    stopping at 16 kHz. The Q of each filter is 3.5, but can be changed. The sampling rate
    is assumed to be 44.1 kHz. 
    
    Parameters
    ----------
    x : ndarray of the input signal samples
    GdB : ndarray containing ten octave band gain values [G0dB,...,G9dB]
    Q : Quality factor vector for each of the NB peaking filters
    
    Returns
    -------
    y : ndarray of output signal samples
    
    Examples
    --------
    >>> # Test with white noise
    >>> w = randn(100000)
    >>> y = ten_band_eq_filt(x,GdB)
    >>> psd(y,2**10,44.1)
    """
    fs = 44100.0 # Hz
    NB = len(GdB)
    if not NB == 10:
        raise ValueError("GdB length not equal to ten")
    Fc = 31.25*2**np.arange(NB)
    B = np.zeros((NB,3))
    A = np.zeros((NB,3))
    
    # Create matrix of cascade coefficients
    for k in range(NB):
        [b,a] = peaking(GdB[k],Fc[k],Q)
        B[k,:] = b
        A[k,:] = a
    # Pass signal x through the cascade of ten filters
    y = np.zeros(len(x))
    for k in range(NB):
        if k == 0:
            y = signal.lfilter(B[k,:],A[k,:],x)
        else:
            y = signal.lfilter(B[k,:],A[k,:],y)
    return y