def fir_remez_bpf(f_stop1, f_pass1, f_pass2, f_stop2, d_pass, d_stop, 
                  fs = 1.0, N_bump=5):
    """
    Design an FIR bandpass filter using remez with order
    determination. The filter order is determined based on 
    f_stop1 Hz, f_pass1 Hz, f_pass2 Hz, f_stop2 Hz, and the 
    desired passband ripple d_pass dB and stopband attenuation
    d_stop dB all relative to a sampling rate of fs Hz.

    Mark Wickert October 2016, updated October 2018
    """
    n, ff, aa, wts = bandpass_order(f_stop1, f_pass1, f_pass2, f_stop2, 
                                  d_pass, d_stop, fsamp=fs)
    # Bump up the order by N_bump to bring down the final d_pass & d_stop
    N_taps = n
    N_taps += N_bump
    b = signal.remez(N_taps, ff, aa[0::2], wts,Hz=2)
    print('Remez filter taps = %d.' % N_taps)
    return b