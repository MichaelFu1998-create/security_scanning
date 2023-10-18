def BPSK_tx(N_bits,Ns,ach_fc=2.0,ach_lvl_dB=-100,pulse='rect',alpha = 0.25,M=6):
    """
    Generates biphase shift keyed (BPSK) transmitter with adjacent channel interference.

    Generates three BPSK signals with rectangular or square root raised cosine (SRC) 
    pulse shaping of duration N_bits and Ns samples per bit. The desired signal is
    centered on f = 0, which the adjacent channel signals to the left and right
    are also generated at dB level relative to the desired signal. Used in the 
    digital communications Case Study supplement.

    Parameters
    ----------
    N_bits : the number of bits to simulate
    Ns : the number of samples per bit
    ach_fc : the frequency offset of the adjacent channel signals (default 2.0)
    ach_lvl_dB : the level of the adjacent channel signals in dB (default -100)
    pulse : the pulse shape 'rect' or 'src'
    alpha : square root raised cosine pulse shape factor (default = 0.25)
    M : square root raised cosine pulse truncation factor (default = 6)

    Returns
    -------
    x : ndarray of the composite signal x0 + ach_lvl*(x1p + x1m)
    b : the transmit pulse shape 
    data0 : the data bits used to form the desired signal; used for error checking

    Notes
    -----

    Examples
    --------
    >>> x,b,data0 = BPSK_tx(1000,10,'src')
    """
    x0,b,data0 = NRZ_bits(N_bits,Ns,pulse,alpha,M)
    x1p,b,data1p = NRZ_bits(N_bits,Ns,pulse,alpha,M)
    x1m,b,data1m = NRZ_bits(N_bits,Ns,pulse,alpha,M)
    n = np.arange(len(x0))
    x1p = x1p*np.exp(1j*2*np.pi*ach_fc/float(Ns)*n)
    x1m = x1m*np.exp(-1j*2*np.pi*ach_fc/float(Ns)*n)
    ach_lvl = 10**(ach_lvl_dB/20.)
    return x0 + ach_lvl*(x1p + x1m), b, data0