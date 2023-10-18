def eye_plot(x,L,S=0):
    """
    Eye pattern plot of a baseband digital communications waveform.

    The signal must be real, but can be multivalued in terms of the underlying
    modulation scheme. Used for BPSK eye plots in the Case Study article.

    Parameters
    ----------
    x : ndarray of the real input data vector/array
    L : display length in samples (usually two symbols)
    S : start index

    Returns
    -------
    None : A plot window opens containing the eye plot
    
    Notes
    -----
    Increase S to eliminate filter transients.
    
    Examples
    --------
    1000 bits at 10 samples per bit with 'rc' shaping.

    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import digitalcom as dc
    >>> x,b, data = dc.NRZ_bits(1000,10,'rc')
    >>> dc.eye_plot(x,20,60)
    >>> plt.show()
    """
    plt.figure(figsize=(6,4))
    idx = np.arange(0,L+1)
    plt.plot(idx,x[S:S+L+1],'b')
    k_max = int((len(x) - S)/L)-1
    for k in range(1,k_max):
         plt.plot(idx,x[S+k*L:S+L+1+k*L],'b')
    plt.grid()
    plt.xlabel('Time Index - n')
    plt.ylabel('Amplitude')
    plt.title('Eye Plot')
    return 0