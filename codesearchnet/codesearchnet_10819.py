def GMSK_bb(N_bits, Ns, MSK = 0,BT = 0.35):
    """
    MSK/GMSK Complex Baseband Modulation
    x,data = gmsk(N_bits, Ns, BT = 0.35, MSK = 0)

    Parameters
    ----------
    N_bits : number of symbols processed
    Ns : the number of samples per bit
    MSK : 0 for no shaping which is standard MSK, MSK <> 0 --> GMSK is generated.
    BT : premodulation Bb*T product which sets the bandwidth of the Gaussian lowpass filter

    Mark Wickert Python version November 2014
    """
    x, b, data = NRZ_bits(N_bits,Ns)
    # pulse length 2*M*Ns
    M = 4
    n = np.arange(-M*Ns,M*Ns+1)
    p = np.exp(-2*np.pi**2*BT**2/np.log(2)*(n/float(Ns))**2);
    p = p/np.sum(p);

    # Gaussian pulse shape if MSK not zero
    if MSK != 0:
        x = signal.lfilter(p,1,x)
    y = np.exp(1j*np.pi/2*np.cumsum(x)/Ns)
    return y, data