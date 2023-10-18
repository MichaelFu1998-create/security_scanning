def bit_errors(tx_data,rx_data,Ncorr = 1024,Ntransient = 0):
    """
    Count bit errors between a transmitted and received BPSK signal.
    Time delay between streams is detected as well as ambiquity resolution
    due to carrier phase lock offsets of :math:`k*\\pi`, k=0,1.
    The ndarray tx_data is Tx 0/1 bits as real numbers I.
    The ndarray rx_data is Rx 0/1 bits as real numbers I.
    Note: Ncorr needs to be even
    """
    
    # Remove Ntransient symbols and level shift to {-1,+1}
    tx_data = 2*tx_data[Ntransient:]-1
    rx_data = 2*rx_data[Ntransient:]-1
    # Correlate the first Ncorr symbols at four possible phase rotations
    R0 = np.fft.ifft(np.fft.fft(rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R1 = np.fft.ifft(np.fft.fft(-1*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    #Place the zero lag value in the center of the array
    R0 = np.fft.fftshift(R0)
    R1 = np.fft.fftshift(R1)
    R0max = np.max(R0.real)
    R1max = np.max(R1.real)
    R = np.array([R0max,R1max])
    Rmax = np.max(R)
    kphase_max = np.where(R == Rmax)[0]
    kmax = kphase_max[0]
    # Correlation lag value is zero at the center of the array
    if kmax == 0:
        lagmax = np.where(R0.real == Rmax)[0] - Ncorr/2
    elif kmax == 1:
        lagmax = np.where(R1.real == Rmax)[0] - Ncorr/2
    taumax = lagmax[0]
    print('kmax =  %d, taumax = %d' % (kmax, taumax))

    # Count bit and symbol errors over the entire input ndarrays
    # Begin by making tx and rx length equal and apply phase rotation to rx
    if taumax < 0:
        tx_data = tx_data[int(-taumax):]
        tx_data = tx_data[:min(len(tx_data),len(rx_data))]
        rx_data = (-1)**kmax*rx_data[:len(tx_data)]
    else:
        rx_data = (-1)**kmax * rx_data[int(taumax):]
        rx_data = rx_data[:min(len(tx_data),len(rx_data))]
        tx_data = tx_data[:len(rx_data)]
    # Convert to 0's and 1's
    Bit_count = len(tx_data)
    tx_I = np.int16((tx_data.real + 1)/2)
    rx_I = np.int16((rx_data.real + 1)/2)
    Bit_errors = tx_I ^ rx_I
    return Bit_count,np.sum(Bit_errors)