def QPSK_rx(fc,N_symb,Rs,EsN0=100,fs=125,lfsr_len=10,phase=0,pulse='src'):
    """
    This function generates
    """
    Ns = int(np.round(fs/Rs))
    print('Ns = ', Ns)
    print('Rs = ', fs/float(Ns))
    print('EsN0 = ', EsN0, 'dB')
    print('phase = ', phase, 'degrees')
    print('pulse = ', pulse)
    x, b, data = QPSK_bb(N_symb,Ns,lfsr_len,pulse)
    # Add AWGN to x
    x = cpx_AWGN(x,EsN0,Ns)
    n = np.arange(len(x))
    xc = x*np.exp(1j*2*np.pi*fc/float(fs)*n) * np.exp(1j*phase)
    return xc, b, data