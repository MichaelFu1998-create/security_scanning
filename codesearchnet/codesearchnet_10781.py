def firwin_kaiser_bpf(f_stop1, f_pass1, f_pass2, f_stop2, d_stop, 
                      fs = 1.0, N_bump=0):
    """
    Design an FIR bandpass filter using the sinc() kernel and
    a Kaiser window. The filter order is determined based on 
    f_stop1 Hz, f_pass1 Hz, f_pass2 Hz, f_stop2 Hz, and the 
    desired stopband attenuation d_stop in dB for both stopbands,
    all relative to a sampling rate of fs Hz.
    Note: the passband ripple cannot be set independent of the
    stopband attenuation.

    Mark Wickert October 2016    
    """
    # Design BPF starting from simple LPF equivalent
    # The upper and lower stopbands are assumed to have 
    # the same attenuation level. The LPF equivalent critical
    # frequencies:
    f_pass = (f_pass2 - f_pass1)/2
    f_stop = (f_stop2 - f_stop1)/2
    # Continue to design equivalent LPF
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
    # Transform LPF to BPF
    f0 = (f_pass2 + f_pass1)/2
    w0 = 2*np.pi*f0/fs
    n = np.arange(len(b_k))
    b_k_bp = 2*b_k*np.cos(w0*(n-M/2))
    print('Kaiser Win filter taps = %d.' % N_taps)
    return b_k_bp