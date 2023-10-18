def MPSK_bb(N_symb,Ns,M,pulse='rect',alpha = 0.25,MM=6):
    """
    Generate a complex baseband MPSK signal with pulse shaping.

    Parameters
    ----------
    N_symb : number of MPSK symbols to produce
    Ns : the number of samples per bit,
    M : MPSK modulation order, e.g., 4, 8, 16, ...
    pulse_type : 'rect' , 'rc', 'src' (default 'rect')
    alpha : excess bandwidth factor(default 0.25)
    MM : single sided pulse duration (default = 6) 

    Returns
    -------
    x : ndarray of the MPSK signal values
    b : ndarray of the pulse shape
    data : ndarray of the underlying data bits

    Notes
    -----
    Pulse shapes include 'rect' (rectangular), 'rc' (raised cosine), 
    'src' (root raised cosine). The actual pulse length is 2*M+1 samples.
    This function is used by BPSK_tx in the Case Study article.

    Examples
    --------
    >>> from sk_dsp_comm import digitalcom as dc
    >>> import scipy.signal as signal
    >>> import matplotlib.pyplot as plt
    >>> x,b,data = dc.MPSK_bb(500,10,8,'src',0.35)
    >>> # Matched filter received signal x
    >>> y = signal.lfilter(b,1,x)
    >>> plt.plot(y.real[12*10:],y.imag[12*10:])
    >>> plt.xlabel('In-Phase')
    >>> plt.ylabel('Quadrature')
    >>> plt.axis('equal')
    >>> # Sample once per symbol
    >>> plt.plot(y.real[12*10::10],y.imag[12*10::10],'r.')
    >>> plt.show()
    """
    data = np.random.randint(0,M,N_symb) 
    xs = np.exp(1j*2*np.pi/M*data)
    x = np.hstack((xs.reshape(N_symb,1),np.zeros((N_symb,int(Ns)-1))))
    x =x.flatten()
    if pulse.lower() == 'rect':
        b = np.ones(int(Ns))
    elif pulse.lower() == 'rc':
        b = rc_imp(Ns,alpha,MM)
    elif pulse.lower() == 'src':
        b = sqrt_rc_imp(Ns,alpha,MM)
    else:
        raise ValueError('pulse type must be rec, rc, or src')
    x = signal.lfilter(b,1,x)
    if M == 4:
        x = x*np.exp(1j*np.pi/4); # For QPSK points in quadrants
    return x,b/float(Ns),data