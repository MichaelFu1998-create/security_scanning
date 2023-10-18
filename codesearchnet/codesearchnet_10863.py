def block_single_error_Pb_bound(j,SNRdB,coded=True,M=2):
    """
    Finds the bit error probability bounds according to Ziemer and Tranter 
    page 656.
    
    parameters:
    -----------
    j: number of parity bits used in single error correction block code
    SNRdB: Eb/N0 values in dB
    coded: Select single error correction code (True) or uncoded (False)
    M: modulation order
    
    returns:
    --------
    Pb: bit error probability bound
    
    """
    Pb = np.zeros_like(SNRdB)
    Ps = np.zeros_like(SNRdB)
    SNR = 10.**(SNRdB/10.)
    n = 2**j-1
    k = n-j
    
    for i,SNRn in enumerate(SNR):
        if coded: # compute Hamming code Ps
            if M == 2:
                Ps[i] = Q_fctn(np.sqrt(k*2.*SNRn/n))
            else:
                Ps[i] = 4./np.log2(M)*(1 - 1/np.sqrt(M))*\
                        np.gaussQ(np.sqrt(3*np.log2(M)/(M-1)*SNRn))/k
        else: # Compute Uncoded Pb
            if M == 2:
                Pb[i] = Q_fctn(np.sqrt(2.*SNRn))
            else:
                Pb[i] = 4./np.log2(M)*(1 - 1/np.sqrt(M))*\
                        np.gaussQ(np.sqrt(3*np.log2(M)/(M-1)*SNRn))
                    
    # Convert symbol error probability to bit error probability
    if coded:
        Pb = ser2ber(M,n,3,1,Ps)
    return Pb