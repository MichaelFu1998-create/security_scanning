def lowpass_order(f_pass, f_stop, dpass_dB, dstop_dB, fsamp = 1):
    """
    Optimal FIR (equal ripple) Lowpass Order Determination
    
    Text reference: Ifeachor, Digital Signal Processing a Practical Approach, 
    second edition, Prentice Hall, 2002.
    Journal paper reference: Herriman et al., Practical Design Rules for Optimum
    Finite Imulse Response Digitl Filters, Bell Syst. Tech. J., vol 52, pp. 
    769-799, July-Aug., 1973.IEEE, 1973.
    """
    dpass = 1 - 10**(-dpass_dB/20)
    dstop = 10**(-dstop_dB/20)
    Df = (f_stop - f_pass)/fsamp
    a1 = 5.309e-3
    a2 = 7.114e-2
    a3 = -4.761e-1
    a4 = -2.66e-3
    a5 = -5.941e-1
    a6 = -4.278e-1
    
    Dinf = np.log10(dstop)*(a1*np.log10(dpass)**2 + a2*np.log10(dpass) + a3) \
           + (a4*np.log10(dpass)**2 + a5*np.log10(dpass) + a6)
    f = 11.01217 + 0.51244*(np.log10(dpass) - np.log10(dstop))
    N = Dinf/Df - f*Df + 1
    ff = 2*np.array([0, f_pass, f_stop, fsamp/2])/fsamp
    aa = np.array([1, 1, 0, 0])
    wts = np.array([1.0, dpass/dstop])
    return int(N), ff, aa, wts