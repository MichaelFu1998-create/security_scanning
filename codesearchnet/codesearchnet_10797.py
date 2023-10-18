def lp_samp(fb,fs,fmax,N,shape='tri',fsize=(6,4)):
    """
    Lowpass sampling theorem plotting function.
    
    Display the spectrum of a sampled signal after setting the bandwidth, 
    sampling frequency, maximum display frequency, and spectral shape.
    
    Parameters
    ----------
    fb : spectrum lowpass bandwidth in Hz
    fs : sampling frequency in Hz
    fmax : plot over [-fmax,fmax]
    shape : 'tri' or 'line'
    N : number of translates, N positive and N negative
    fsize : the size of the figure window, default (6,4)
    
    Returns
    -------
    Nothing : A plot window opens containing the spectrum plot
    
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm.sigsys import lp_samp

    No aliasing as bandwidth 10 Hz < 25/2; fs > fb.

    >>> lp_samp(10,25,50,10)
    >>> plt.show()

    Now aliasing as bandwidth 15 Hz > 25/2; fs < fb.

    >>> lp_samp(15,25,50,10)

    """
    plt.figure(figsize=fsize)
    # define the plot interval
    f = np.arange(-fmax,fmax+fmax/200.,fmax/200.)
    A = 1.0
    line_ampl = A/2.*np.array([0, 1])
    # plot the lowpass spectrum in black
    shapes = ['tri', 'line']
    if shape.lower() not in shapes:
        raise ValueError('shape must be tri or line')
    if shape.lower() == 'tri':
        plt.plot(f,lp_tri(f,fb))
        # overlay positive and negative frequency translates
        for n in range(N):
            plt.plot(f, lp_tri(f - (n + 1) * fs, fb), '--r')
            plt.plot(f, lp_tri(f + (n + 1) * fs, fb), '--g')
    elif shape.lower() == 'line':
        plt.plot([fb, fb],line_ampl,'b', linewidth=2)
        plt.plot([-fb, -fb],line_ampl,'b', linewidth=2)
        # overlay positive and negative frequency translates
        for n in range(N):
            plt.plot([fb+(n+1)*fs, fb+(n+1)*fs],line_ampl,'--r', linewidth=2)
            plt.plot([-fb+(n+1)*fs, -fb+(n+1)*fs],line_ampl,'--r', linewidth=2)
            plt.plot([fb-(n+1)*fs, fb-(n+1)*fs],line_ampl,'--g', linewidth=2)
            plt.plot([-fb-(n+1)*fs, -fb-(n+1)*fs],line_ampl,'--g', linewidth=2)
    plt.ylabel('Spectrum Magnitude')
    plt.xlabel('Frequency in Hz')
    plt.axis([-fmax,fmax,0,1])
    plt.grid()