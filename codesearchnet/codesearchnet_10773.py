def IIR_lpf(f_pass, f_stop, Ripple_pass, Atten_stop, 
            fs = 1.00, ftype = 'butter'):
    """
    Design an IIR lowpass filter using scipy.signal.iirdesign. 
    The filter order is determined based on 
    f_pass Hz, f_stop Hz, and the desired stopband attenuation
    d_stop in dB, all relative to a sampling rate of fs Hz.

    Parameters
    ----------
    f_pass : Passband critical frequency in Hz
    f_stop : Stopband critical frequency in Hz
    Ripple_pass : Filter gain in dB at f_pass
    Atten_stop : Filter attenuation in dB at f_stop
    fs : Sampling rate in Hz
    ftype : Analog prototype from 'butter' 'cheby1', 'cheby2',
            'ellip', and 'bessel'

    Returns
    -------
    b : ndarray of the numerator coefficients
    a : ndarray of the denominator coefficients
    sos : 2D ndarray of second-order section coefficients

    Notes
    -----
    Additionally a text string telling the user the filter order is
    written to the console, e.g., IIR cheby1 order = 8.

    Examples
    --------
    >>> fs = 48000
    >>> f_pass = 5000
    >>> f_stop = 8000
    >>> b_but,a_but,sos_but = IIR_lpf(f_pass,f_stop,0.5,60,fs,'butter')
    >>> b_cheb1,a_cheb1,sos_cheb1 = IIR_lpf(f_pass,f_stop,0.5,60,fs,'cheby1')
    >>> b_cheb2,a_cheb2,sos_cheb2 = IIR_lpf(f_pass,f_stop,0.5,60,fs,'cheby2')
    >>> b_elli,a_elli,sos_elli = IIR_lpf(f_pass,f_stop,0.5,60,fs,'ellip')


    Mark Wickert October 2016
    """
   
    b,a = signal.iirdesign(2*float(f_pass)/fs, 2*float(f_stop)/fs,
                           Ripple_pass, Atten_stop,
                           ftype = ftype, output='ba')
    sos = signal.iirdesign(2*float(f_pass)/fs, 2*float(f_stop)/fs,
                           Ripple_pass, Atten_stop,
                           ftype = ftype, output='sos')
    tag = 'IIR ' + ftype + ' order'
    print('%s = %d.' % (tag,len(a)-1))
    return b, a, sos