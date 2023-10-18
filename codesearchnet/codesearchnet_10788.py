def CIC(M, K):
    """
    A functional form implementation of a cascade of integrator comb (CIC) filters.

    Parameters
    ----------
    M : Effective number of taps per section (typically the decimation factor).
    K : The number of CIC sections cascaded (larger K gives the filter a wider image rejection bandwidth).

    Returns
    -------
    b : FIR filter coefficients for a simple direct form implementation using the filter() function.

    Notes
    -----
    Commonly used in multirate signal processing digital down-converters and digital up-converters. A true CIC filter
    requires no multiplies, only add and subtract operations. The functional form created here is a simple FIR requiring
    real coefficient multiplies via filter().

    Mark Wickert July 2013
    """

    if K == 1:
        b = np.ones(M)
    else:
        h = np.ones(M)
        b = h
        for i in range(1, K):
            b = signal.convolve(b, h)  # cascade by convolving impulse responses

    # Make filter have unity gain at DC
    return b / np.sum(b)