def ten_band_eq_resp(GdB,Q=3.5):
    """
    Create a frequency response magnitude plot in dB of a ten band equalizer
    using a semilogplot (semilogx()) type plot
    
    
    Parameters
    ----------
    GdB : Gain vector for 10 peaking filters [G0,...,G9]
    Q : Quality factor for each peaking filter (default 3.5)
    
    Returns
    -------
    Nothing : two plots are created
    
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import sigsys as ss
    >>> ss.ten_band_eq_resp([0,10.0,0,0,-1,0,5,0,-4,0])
    >>> plt.show()
    """
    fs = 44100.0 # Hz
    NB = len(GdB)
    if not NB == 10:
        raise ValueError("GdB length not equal to ten")
    Fc = 31.25*2**np.arange(NB)
    B = np.zeros((NB,3));
    A = np.zeros((NB,3));
    
    # Create matrix of cascade coefficients
    for k in range(NB):
        b,a = peaking(GdB[k],Fc[k],Q,fs)
        B[k,:] = b
        A[k,:] = a
    # Create the cascade frequency response
    F = np.logspace(1,np.log10(20e3),1000)
    H = np.ones(len(F))*np.complex(1.0,0.0)
    for k in range(NB):
       w,Htemp = signal.freqz(B[k,:],A[k,:],2*np.pi*F/fs)
       H *= Htemp
    plt.figure(figsize=(6,4))
    plt.subplot(211)
    plt.semilogx(F,20*np.log10(abs(H)))
    plt.axis([10, fs/2, -12, 12])
    plt.grid()
    plt.title('Ten-Band Equalizer Frequency Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.subplot(212)
    plt.stem(np.arange(NB),GdB,'b','bs')
    #plt.bar(np.arange(NB)-.1,GdB,0.2)
    plt.axis([0, NB-1, -12, 12])
    plt.xlabel('Equalizer Band Number')
    plt.ylabel('Gain Set (dB)')
    plt.grid()