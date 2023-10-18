def bandpass_order(f_stop1, f_pass1, f_pass2, f_stop2, dpass_dB, dstop_dB, fsamp = 1):
    """
    Optimal FIR (equal ripple) Bandpass Order Determination
    
    Text reference: Ifeachor, Digital Signal Processing a Practical Approach, 
    second edition, Prentice Hall, 2002.
    Journal paper reference: F. Mintzer & B. Liu, Practical Design Rules for Optimum
    FIR Bandpass Digital Filters, IEEE Transactions on Acoustics and Speech, pp. 
    204-206, April,1979.
    """
    dpass = 1 - 10**(-dpass_dB/20)
    dstop = 10**(-dstop_dB/20)
    Df1 = (f_pass1 - f_stop1)/fsamp
    Df2 = (f_stop2 - f_pass2)/fsamp
    b1 = 0.01201
    b2 = 0.09664
    b3 = -0.51325
    b4 = 0.00203
    b5 = -0.5705
    b6 = -0.44314
    
    Df = min(Df1, Df2)
    Cinf = np.log10(dstop)*(b1*np.log10(dpass)**2 + b2*np.log10(dpass) + b3) \
           + (b4*np.log10(dpass)**2 + b5*np.log10(dpass) + b6)
    g = -14.6*np.log10(dpass/dstop) - 16.9
    N = Cinf/Df + g*Df + 1
    ff = 2*np.array([0, f_stop1, f_pass1, f_pass2, f_stop2, fsamp/2])/fsamp
    aa = np.array([0, 0, 1, 1, 0, 0])
    wts = np.array([dpass/dstop, 1, dpass/dstop])
    return int(N), ff, aa, wts