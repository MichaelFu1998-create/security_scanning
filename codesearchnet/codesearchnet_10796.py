def OS_filter(x,h,N,mode=0):
    """
    Overlap and save transform domain FIR filtering.
    
    This function implements the classical overlap and save method of
    transform domain filtering using a length P FIR filter.
    
    Parameters
    ----------
    x : input signal to be filtered as an ndarray
    h : FIR filter coefficients as an ndarray of length P
    N : FFT size > P, typically a power of two
    mode : 0 or 1, when 1 returns a diagnostic matrix
    
    Returns
    -------
    y : the filtered output as an ndarray
    y_mat : an ndarray whose rows are the individual overlap outputs.
    
    Notes
    -----
    y_mat is used for diagnostics and to gain understanding of the algorithm.
    
    Examples
    --------
    >>> n = arange(0,100)
    >>> x = cos(2*pi*0.05*n)
    >>> b = ones(10)
    >>> y = OS_filter(x,h,N)
    >>> # set mode = 1
    >>> y, y_mat = OS_filter(x,h,N,1)
    """
    
    P = len(h)
    # zero pad start of x so first frame can recover first true samples of x
    x = np.hstack((np.zeros(P-1),x))
    L = N - P + 1
    Nx = len(x)
    Nframe = int(np.ceil(Nx/float(L)))
    # zero pad end of x to full number of frames needed
    x = np.hstack((x,np.zeros(Nframe*L-Nx)))
    y = np.zeros(int(Nframe*N))
    # create an instrumentation matrix to observe the overlap and save behavior
    y_mat = np.zeros((Nframe,int(Nframe*N)))

    H = fft.fft(h,N)
    # begin the filtering operation
    for k in range(Nframe):
        xk = x[k*L:k*L+N]
        Xk = fft.fft(xk,N)
        Yk = H*Xk
        yk = np.real(fft.ifft(Yk)) # imag part should be zero
        y[k*L+P-1:k*L+N] = yk[P-1:]
        y_mat[k,k*L:k*L+N] = yk
    if mode == 1:
        return y[P-1:Nx], y_mat[:,P-1:Nx]
    else:
        return y[P-1:Nx]