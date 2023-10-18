def QAM_bb(N_symb,Ns,mod_type='16qam',pulse='rect',alpha=0.35):
    """
    QAM_BB_TX: A complex baseband transmitter 
    x,b,tx_data = QAM_bb(K,Ns,M)

    //////////// Inputs //////////////////////////////////////////////////
      N_symb = the number of symbols to process
          Ns = number of samples per symbol
    mod_type = modulation type: qpsk, 16qam, 64qam, or 256qam
       alpha = squareroot raised codine pulse shape bandwidth factor.
               For DOCSIS alpha = 0.12 to 0.18. In general alpha can 
               range over 0 < alpha < 1.
         SRC = pulse shape: 0-> rect, 1-> SRC
    //////////// Outputs /////////////////////////////////////////////////
           x = complex baseband digital modulation
           b = transmitter shaping filter, rectangle or SRC
     tx_data = xI+1j*xQ = inphase symbol sequence + 
               1j*quadrature symbol sequence

    Mark Wickert November 2014
    """
    # Filter the impulse train waveform with a square root raised
    # cosine pulse shape designed as follows:

    # Design the filter to be of duration 12 symbols and
    # fix the excess bandwidth factor at alpha = 0.35
    # If SRC = 0 use a simple rectangle pulse shape
    if pulse.lower() == 'src':
        b = sqrt_rc_imp(Ns,alpha,6)
    elif pulse.lower() == 'rc':
        b = rc_imp(Ns,alpha,6)    
    elif pulse.lower() == 'rect':
        b = np.ones(int(Ns)) #alt. rect. pulse shape
    else:
        raise ValueError('pulse shape must be src, rc, or rect')
        
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

    # Create random symbols for the I & Q channels
    xI = np.random.randint(0,M,N_symb)
    xI = 2*xI - (M-1)
    xQ = np.random.randint(0,M,N_symb)
    xQ = 2*xQ - (M-1)
    # Employ differential encoding to counter phase ambiquities
    # Create a zero padded (interpolated by Ns) symbol sequence.
    # This prepares the symbol sequence for arbitrary pulse shaping.
    symbI = np.hstack((xI.reshape(N_symb,1),np.zeros((N_symb,int(Ns)-1))))
    symbI = symbI.flatten()
    symbQ = np.hstack((xQ.reshape(N_symb,1),np.zeros((N_symb,int(Ns)-1))))
    symbQ = symbQ.flatten()
    symb = symbI + 1j*symbQ
    if M > 2:
        symb /= (M-1)
    
    # The impulse train waveform contains one pulse per Ns (or Ts) samples
    # imp_train = [ones(K,1) zeros(K,Ns-1)]';
    # imp_train = reshape(imp_train,Ns*K,1);

    # Filter the impulse train signal
    x = signal.lfilter(b,1,symb)
    x = x.flatten() # out is a 1D vector
    # Scale shaping filter to have unity DC gain
    b = b/sum(b)
    return x, b, xI+1j*xQ