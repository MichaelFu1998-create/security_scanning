def lp_tri(f, fb):
    """
    Triangle spectral shape function used by :func:`lp_samp`.

    Parameters
    ----------
    f : ndarray containing frequency samples
    fb : the bandwidth as a float constant
    
    Returns
    -------
    x : ndarray of spectrum samples for a single triangle shape

    Notes
    -----
    This is a support function for the lowpass spectrum plotting function
    :func:`lp_samp`.

    Examples
    --------
    >>> x = lp_tri(f, fb)
    """

    x = np.zeros(len(f))
    for k in range(len(f)):
        if abs(f[k]) <= fb:
            x[k] = 1 - abs(f[k])/float(fb)
    return x