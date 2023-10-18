def firwin_kaiser_lpf(f_pass, f_stop, d_stop, fs = 1.0, N_bump=0):
    """
    Design an FIR lowpass filter using the sinc() kernel and
    a Kaiser window. The filter order is determined based on 
    f_pass Hz, f_stop Hz, and the desired stopband attenuation
    d_stop in dB, all relative to a sampling rate of fs Hz.
    Note: the passband ripple cannot be set independent of the
    stopband attenuation.

    Mark Wickert October 2016
    """
    wc = 2*np.pi*(f_pass + f_stop)/2/fs
    delta_w = 2*np.pi*(f_stop - f_pass)/fs
    # Find the filter order
    M = np.ceil((d_stop - 8)/(2.285*delta_w))
    # Adjust filter order up or down as needed
    M += N_bump
    N_taps = M + 1
    # Obtain the Kaiser window
    beta = signal.kaiser_beta(d_stop)
    w_k = signal.kaiser(N_taps,beta)
    n = np.arange(N_taps)
    b_k = wc/np.pi*np.sinc(wc/np.pi*(n-M/2)) * w_k
    b_k /= np.sum(b_k)
    print('Kaiser Win filter taps = %d.' % N_taps)
    return b_k