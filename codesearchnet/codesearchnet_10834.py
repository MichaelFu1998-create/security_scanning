def mux_pilot_blocks(IQ_data, Np):
    """
    Parameters
    ----------
    IQ_data : a 2D array of input QAM symbols with the columns
               representing the NF carrier frequencies and each
               row the QAM symbols used to form an OFDM symbol
    Np : the period of the pilot blocks; e.g., a pilot block is
               inserted every Np OFDM symbols (Np-1 OFDM data symbols
               of width Nf are inserted in between the pilot blocks.

    Returns
    -------
    IQ_datap : IQ_data with pilot blocks inserted

    See Also
    --------
    OFDM_tx

    Notes
    -----
    A helper function called by :func:`OFDM_tx` that inserts pilot block for use
    in channel estimation when a delay spread channel is present.
    """
    N_OFDM = IQ_data.shape[0]
    Npb = N_OFDM // (Np - 1)
    N_OFDM_rem = N_OFDM - Npb * (Np - 1)
    Nf = IQ_data.shape[1]
    IQ_datap = np.zeros((N_OFDM + Npb + 1, Nf), dtype=np.complex128)
    pilots = np.ones(Nf)  # The pilot symbol is simply 1 + j0
    for k in range(Npb):
        IQ_datap[Np * k:Np * (k + 1), :] = np.vstack((pilots,
                                                      IQ_data[(Np - 1) * k:(Np - 1) * (k + 1), :]))
    IQ_datap[Np * Npb:Np * (Npb + N_OFDM_rem), :] = np.vstack((pilots,
                                                               IQ_data[(Np - 1) * Npb:, :]))
    return IQ_datap