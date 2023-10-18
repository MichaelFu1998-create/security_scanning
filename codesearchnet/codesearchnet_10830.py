def PCM_encode(x,N_bits):
    """
    Parameters
    ----------
    x : signal samples to be PCM encoded
    N_bits ; bit precision of PCM samples

    Returns
    -------
    x_bits = encoded serial bit stream of 0/1 values. MSB first.

    Mark Wickert, Mark 2015
    """
    xq = np.int16(np.rint(x*2**(N_bits-1)))
    x_bits = np.zeros((N_bits,len(xq)))
    for k, xk in enumerate(xq):
        x_bits[:,k] = to_bin(xk,N_bits)
    # Reshape into a serial bit stream
    x_bits = np.reshape(x_bits,(1,len(x)*N_bits),'F')
    return np.int16(x_bits.flatten())