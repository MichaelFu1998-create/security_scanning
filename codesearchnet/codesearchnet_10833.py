def PCM_decode(x_bits,N_bits):
    """
    Parameters
    ----------
    x_bits : serial bit stream of 0/1 values. The length of
             x_bits must be a multiple of N_bits
    N_bits : bit precision of PCM samples

    Returns
    -------
      xhat : decoded PCM signal samples

    Mark Wickert, March 2015
    """
    N_samples = len(x_bits)//N_bits
    # Convert serial bit stream into parallel words with each 
    # column holdingthe N_bits binary sample value
    xrs_bits = x_bits.copy()
    xrs_bits = np.reshape(xrs_bits,(N_bits,N_samples),'F')
    # Convert N_bits binary words into signed integer values
    xq = np.zeros(N_samples)
    w = 2**np.arange(N_bits-1,-1,-1) # binary weights for bin 
                                     # to dec conversion
    for k in range(N_samples):
       xq[k] = np.dot(xrs_bits[:,k],w) - xrs_bits[0,k]*2**N_bits
    return xq/2**(N_bits-1)