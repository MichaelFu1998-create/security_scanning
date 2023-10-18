def fir_remez_bsf(f_pass1, f_stop1, f_stop2, f_pass2, d_pass, d_stop, 
                  fs = 1.0, N_bump=5):
    """
    Design an FIR bandstop filter using remez with order
    determination. The filter order is determined based on 
    f_pass1 Hz, f_stop1 Hz, f_stop2 Hz, f_pass2 Hz, and the 
    desired passband ripple d_pass dB and stopband attenuation
    d_stop dB all relative to a sampling rate of fs Hz.

    Mark Wickert October 2016, updated October 2018
    """
    n, ff, aa, wts = bandstop_order(f_pass1, f_stop1, f_stop2, f_pass2, 
                                    d_pass, d_stop, fsamp=fs)
    # Bump up the order by N_bump to bring down the final d_pass & d_stop
    # Initially make sure the number of taps is even so N_bump needs to be odd
    if np.mod(n,2) != 0:
        n += 1
    N_taps = n
    N_taps += N_bump
    b = signal.remez(N_taps, ff, aa[0::2], wts, Hz=2,
                     maxiter = 25, grid_density = 16)
    print('N_bump must be odd to maintain odd filter length')
    print('Remez filter taps = %d.' % N_taps)
    return b