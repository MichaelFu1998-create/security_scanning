def fft(values, freq=None, timestamps=None, fill_missing=False):
    """
    Adds options to :func:`scipy.fftpack.rfft`:

    * *freq* is the frequency the samples were taken at
    * *timestamps* is the time the samples were taken, to help with filling in missing data if *fill_missing* is true
    """
    # ======================================
    # Get frequency
    # ======================================
    if freq is None:
        from .. import qt
        freq = qt.getDouble(title='Fourier Analysis', text='Frequency samples taken at:', min=0, decimals=2, value=1.0)
        freq = freq.input
    
    if fill_missing:
        (t_x, x_filled) = fill_missing_timestamps(timestamps, values)
    else:
        x_filled = values
        
    num_samples = _np.size(x_filled)
    xfft = _sp.fftpack.rfft(x_filled)
    
    factor = freq/num_samples
    num_fft = _np.size(xfft)
    f = factor * _np.linspace(1, num_fft, num_fft)
    
    xpow = _np.abs(xfft*_np.conj(xfft))

    # ======================================
    # No DC term
    # ======================================
    xpow = xpow[1:]
    f = f[1:]

    return (f, xpow)