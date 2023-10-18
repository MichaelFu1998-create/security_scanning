def RZ_bits(N_bits,Ns,pulse='rect',alpha = 0.25,M=6):
    """
    Generate return-to-zero (RZ) data bits with pulse shaping.

    A baseband digital data signal using +/-1 amplitude signal values
    and including pulse shaping.

    Parameters
    ----------
    N_bits : number of RZ {0,1} data bits to produce
    Ns : the number of samples per bit,
    pulse_type : 'rect' , 'rc', 'src' (default 'rect')
    alpha : excess bandwidth factor(default 0.25)
    M : single sided pulse duration (default = 6) 

    Returns
    -------
    x : ndarray of the RZ signal values
    b : ndarray of the pulse shape
    data : ndarray of the underlying data bits

    Notes
    -----
    Pulse shapes include 'rect' (rectangular), 'rc' (raised cosine), 
    'src' (root raised cosine). The actual pulse length is 2*M+1 samples.
    This function is used by BPSK_tx in the Case Study article.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from numpy import arange
    >>> from sk_dsp_comm.digitalcom import RZ_bits
    >>> x,b,data = RZ_bits(100,10)
    >>> t = arange(len(x))
    >>> plt.plot(t,x)
    >>> plt.ylim([-0.01, 1.01])
    >>> plt.show()
    """
    data = np.random.randint(0,2,N_bits) 
    x = np.hstack((data.reshape(N_bits,1),np.zeros((N_bits,int(Ns)-1))))
    x =x.flatten()
    if pulse.lower() == 'rect':
        b = np.ones(int(Ns))
    elif pulse.lower() == 'rc':
        b = rc_imp(Ns,alpha,M)
    elif pulse.lower() == 'src':
        b = sqrt_rc_imp(Ns,alpha,M)
    else:
        print('pulse type must be rec, rc, or src')
    x = signal.lfilter(b,1,x)
    return x,b/float(Ns),data