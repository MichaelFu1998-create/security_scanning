def QPSK_BEP(tx_data,rx_data,Ncorr = 1024,Ntransient = 0):
    """
    Count bit errors between a transmitted and received QPSK signal.
    Time delay between streams is detected as well as ambiquity resolution
    due to carrier phase lock offsets of :math:`k*\\frac{\\pi}{4}`, k=0,1,2,3.
    The ndarray sdata is Tx +/-1 symbols as complex numbers I + j*Q.
    The ndarray data is Rx +/-1 symbols as complex numbers I + j*Q.
    Note: Ncorr needs to be even
    """
    
    #Remove Ntransient symbols
    tx_data = tx_data[Ntransient:]
    rx_data = rx_data[Ntransient:]
    #Correlate the first Ncorr symbols at four possible phase rotations
    R0 = np.fft.ifft(np.fft.fft(rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R1 = np.fft.ifft(np.fft.fft(1j*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R2 = np.fft.ifft(np.fft.fft(-1*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R3 = np.fft.ifft(np.fft.fft(-1j*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    #Place the zero lag value in the center of the array
    R0 = np.fft.fftshift(R0)
    R1 = np.fft.fftshift(R1)
    R2 = np.fft.fftshift(R2)
    R3 = np.fft.fftshift(R3)
    R0max = np.max(R0.real)
    R1max = np.max(R1.real)
    R2max = np.max(R2.real)
    R3max = np.max(R3.real)
    R = np.array([R0max,R1max,R2max,R3max])
    Rmax = np.max(R)
    kphase_max = np.where(R == Rmax)[0]
    kmax = kphase_max[0]
    #Correlation lag value is zero at the center of the array
    if kmax == 0:
        lagmax = np.where(R0.real == Rmax)[0] - Ncorr/2
    elif kmax == 1:
        lagmax = np.where(R1.real == Rmax)[0] - Ncorr/2
    elif kmax == 2: 
        lagmax = np.where(R2.real == Rmax)[0] - Ncorr/2
    elif kmax == 3:
        lagmax = np.where(R3.real == Rmax)[0] - Ncorr/2
    taumax = lagmax[0]
    print('kmax =  %d, taumax = %d' % (kmax, taumax))
    # Count bit and symbol errors over the entire input ndarrays
    # Begin by making tx and rx length equal and apply phase rotation to rx
    if taumax < 0:
        tx_data = tx_data[-taumax:]
        tx_data = tx_data[:min(len(tx_data),len(rx_data))]
        rx_data = 1j**kmax*rx_data[:len(tx_data)]
    else:
        rx_data = 1j**kmax*rx_data[taumax:]
        rx_data = rx_data[:min(len(tx_data),len(rx_data))]
        tx_data = tx_data[:len(rx_data)]
    #Convert to 0's and 1's
    S_count = len(tx_data)
    tx_I = np.int16((tx_data.real + 1)/2)
    tx_Q = np.int16((tx_data.imag + 1)/2)
    rx_I = np.int16((rx_data.real + 1)/2)
    rx_Q = np.int16((rx_data.imag + 1)/2)
    I_errors = tx_I ^ rx_I
    Q_errors = tx_Q ^ rx_Q
    #A symbol errors occurs when I or Q or both are in error
    S_errors = I_errors | Q_errors
    #return 0
    return S_count,np.sum(I_errors),np.sum(Q_errors),np.sum(S_errors)