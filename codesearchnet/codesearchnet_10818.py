def QAM_SEP(tx_data,rx_data,mod_type,Ncorr = 1024,Ntransient = 0,SEP_disp=True):
    """
    Nsymb, Nerr, SEP_hat =
    QAM_symb_errors(tx_data,rx_data,mod_type,Ncorr = 1024,Ntransient = 0)
    
    Count symbol errors between a transmitted and received QAM signal.
    The received symbols are assumed to be soft values on a unit square.
    Time delay between streams is detected.
    The ndarray tx_data is Tx complex symbols.
    The ndarray rx_data is Rx complex symbols.
    Note: Ncorr needs to be even
    """
    #Remove Ntransient symbols and makes lengths equal
    tx_data = tx_data[Ntransient:]
    rx_data = rx_data[Ntransient:]
    Nmin = min([len(tx_data),len(rx_data)])
    tx_data = tx_data[:Nmin]
    rx_data = rx_data[:Nmin]
    
    # Perform level translation and quantize the soft symbol values
    if mod_type.lower() == 'qpsk':
        M = 2 # bits per symbol
    elif mod_type.lower() == '16qam':
        M = 4
    elif mod_type.lower() == '64qam':
        M = 8
    elif mod_type.lower() == '256qam':
        M = 16
    else:
        raise ValueError('Unknown mod_type')
    rx_data = np.rint((M-1)*(rx_data + (1+1j))/2.)
    # Fix-up edge points real part
    s1r = np.nonzero(np.ravel(rx_data.real > M - 1))[0]
    s2r = np.nonzero(np.ravel(rx_data.real < 0))[0]
    rx_data.real[s1r] = (M - 1)*np.ones(len(s1r))
    rx_data.real[s2r] = np.zeros(len(s2r))
    # Fix-up edge points imag part
    s1i = np.nonzero(np.ravel(rx_data.imag > M - 1))[0]
    s2i = np.nonzero(np.ravel(rx_data.imag < 0))[0]
    rx_data.imag[s1i] = (M - 1)*np.ones(len(s1i))
    rx_data.imag[s2i] = np.zeros(len(s2i))
    rx_data = 2*rx_data - (M - 1)*(1 + 1j)
    #Correlate the first Ncorr symbols at four possible phase rotations
    R0,lags = xcorr(rx_data,tx_data,Ncorr)
    R1,lags = xcorr(rx_data*(1j)**1,tx_data,Ncorr) 
    R2,lags = xcorr(rx_data*(1j)**2,tx_data,Ncorr) 
    R3,lags = xcorr(rx_data*(1j)**3,tx_data,Ncorr) 
    #Place the zero lag value in the center of the array
    R0max = np.max(R0.real)
    R1max = np.max(R1.real)
    R2max = np.max(R2.real)
    R3max = np.max(R3.real)
    R = np.array([R0max,R1max,R2max,R3max])
    Rmax = np.max(R)
    kphase_max = np.where(R == Rmax)[0]
    kmax = kphase_max[0]
    #Find correlation lag value is zero at the center of the array
    if kmax == 0:
        lagmax = lags[np.where(R0.real == Rmax)[0]]
    elif kmax == 1:
        lagmax = lags[np.where(R1.real == Rmax)[0]]
    elif kmax == 2:
        lagmax = lags[np.where(R2.real == Rmax)[0]]
    elif kmax == 3:
        lagmax = lags[np.where(R3.real == Rmax)[0]]
    taumax = lagmax[0]
    if SEP_disp:
        print('Phase ambiquity = (1j)**%d, taumax = %d' % (kmax, taumax))
    #Count symbol errors over the entire input ndarrays
    #Begin by making tx and rx length equal and apply 
    #phase rotation to rx_data
    if taumax < 0:
        tx_data = tx_data[-taumax:]
        tx_data = tx_data[:min(len(tx_data),len(rx_data))]
        rx_data = (1j)**kmax*rx_data[:len(tx_data)]
    else:
        rx_data = (1j)**kmax*rx_data[taumax:]
        rx_data = rx_data[:min(len(tx_data),len(rx_data))]
        tx_data = tx_data[:len(rx_data)]
    #Convert QAM symbol difference to symbol errors
    errors = np.int16(abs(rx_data-tx_data))
    # Detect symbols errors
    # Could decode bit errors from symbol index difference
    idx = np.nonzero(np.ravel(errors != 0))[0]
    if SEP_disp:
        print('Symbols = %d, Errors %d, SEP = %1.2e' \
               % (len(errors), len(idx), len(idx)/float(len(errors))))
    return  len(errors), len(idx), len(idx)/float(len(errors))