def farrow_resample(x, fs_old, fs_new):
    """
    Parameters
    ----------
    x : Input list representing a signal vector needing resampling.
    fs_old : Starting/old sampling frequency.
    fs_new : New sampling frequency.

    Returns
    -------
    y : List representing the signal vector resampled at the new frequency.

    Notes
    -----

    A cubic interpolator using a Farrow structure is used resample the
    input data at a new sampling rate that may be an irrational multiple of
    the input sampling rate.

    Time alignment can be found for a integer value M, found with the following:

    .. math:: f_{s,out} = f_{s,in} (M - 1) / M
    
    The filter coefficients used here and a more comprehensive listing can be
    found in H. Meyr, M. Moeneclaey, & S. Fechtel, "Digital Communication 
    Receivers," Wiley, 1998, Chapter 9, pp. 521-523.
    
    Another good paper on variable interpolators is: L. Erup, F. Gardner, &
    R. Harris, "Interpolation in Digital Modems--Part II: Implementation
    and Performance," IEEE Comm. Trans., June 1993, pp. 998-1008.
    
    A founding paper on the subject of interpolators is: C. W. Farrow, "A
    Continuously variable Digital Delay Element," Proceedings of the IEEE
    Intern. Symp. on Circuits Syst., pp. 2641-2645, June 1988.
    
    Mark Wickert April 2003, recoded to Python November 2013

    Examples
    --------

    The following example uses a QPSK signal with rc pulse shaping, and time alignment at M = 15.

    >>> import matplotlib.pyplot as plt
    >>> from numpy import arange
    >>> from sk_dsp_comm import digitalcom as dc
    >>> Ns = 8
    >>> Rs = 1.
    >>> fsin = Ns*Rs
    >>> Tsin = 1 / fsin
    >>> N = 200
    >>> ts = 1
    >>> x, b, data = dc.MPSK_bb(N+12, Ns, 4, 'rc')
    >>> x = x[12*Ns:]
    >>> xxI = x.real
    >>> M = 15
    >>> fsout = fsin * (M-1) / M
    >>> Tsout = 1. / fsout
    >>> xI = dc.farrow_resample(xxI, fsin, fsin)
    >>> tx = arange(0, len(xI)) / fsin
    >>> yI = dc.farrow_resample(xxI, fsin, fsout)
    >>> ty = arange(0, len(yI)) / fsout
    >>> plt.plot(tx - Tsin, xI)
    >>> plt.plot(tx[ts::Ns] - Tsin, xI[ts::Ns], 'r.')
    >>> plt.plot(ty[ts::Ns] - Tsout, yI[ts::Ns], 'g.')
    >>> plt.title(r'Impact of Asynchronous Sampling')
    >>> plt.ylabel(r'Real Signal Amplitude')
    >>> plt.xlabel(r'Symbol Rate Normalized Time')
    >>> plt.xlim([0, 20])
    >>> plt.grid()
    >>> plt.show()
    """
    
    #Cubic interpolator over 4 samples.
    #The base point receives a two sample delay.
    v3 = signal.lfilter([1/6., -1/2., 1/2., -1/6.],[1],x)
    v2 = signal.lfilter([0, 1/2., -1, 1/2.],[1],x)
    v1 = signal.lfilter([-1/6., 1, -1/2., -1/3.],[1],x)
    v0 = signal.lfilter([0, 0, 1],[1],x)
    
    Ts_old = 1/float(fs_old)
    Ts_new = 1/float(fs_new)
    
    T_end = Ts_old*(len(x)-3)
    t_new = np.arange(0,T_end+Ts_old,Ts_new)
    if x.dtype == np.dtype('complex128') or x.dtype == np.dtype('complex64'):
        y = np.zeros(len(t_new)) + 1j*np.zeros(len(t_new))
    else:
        y = np.zeros(len(t_new))

    for n in range(len(t_new)):
        n_old = int(np.floor(n*Ts_new/Ts_old))
        mu = (n*Ts_new - n_old*Ts_old)/Ts_old
        # Combine outputs
        y[n] = ((v3[n_old+1]*mu + v2[n_old+1])*mu
                + v1[n_old+1])*mu + v0[n_old+1]
    return y