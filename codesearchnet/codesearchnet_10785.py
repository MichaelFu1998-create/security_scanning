def fir_remez_hpf(f_stop, f_pass, d_pass, d_stop, fs = 1.0, N_bump=5):
    """
    Design an FIR highpass filter using remez with order
    determination. The filter order is determined based on 
    f_pass Hz, fstop Hz, and the desired passband ripple 
    d_pass dB and stopband attenuation d_stop dB all 
    relative to a sampling rate of fs Hz.

    Mark Wickert October 2016, updated October 2018
    """
    # Transform HPF critical frequencies to lowpass equivalent
    f_pass_eq = fs/2. - f_pass
    f_stop_eq = fs/2. - f_stop
    # Design LPF equivalent
    n, ff, aa, wts = lowpass_order(f_pass_eq, f_stop_eq, d_pass, d_stop, fsamp=fs)
    # Bump up the order by N_bump to bring down the final d_pass & d_stop
    N_taps = n
    N_taps += N_bump
    b = signal.remez(N_taps, ff, aa[0::2], wts,Hz=2)
    # Transform LPF equivalent to HPF
    n = np.arange(len(b))
    b *= (-1)**n
    print('Remez filter taps = %d.' % N_taps)
    return b