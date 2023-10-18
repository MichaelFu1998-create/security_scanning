def firwin_bpf(N_taps, f1, f2, fs = 1.0, pass_zero=False):
    """
    Design a windowed FIR bandpass filter in terms of passband
    critical frequencies f1 < f2 in Hz relative to sampling rate
    fs in Hz. The number of taps must be provided.

    Mark Wickert October 2016
    """
    return signal.firwin(N_taps,2*(f1,f2)/fs,pass_zero=pass_zero)