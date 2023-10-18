def otsu_threshold(data, bins=255):
    """
    Otsu threshold on data.

    Otsu thresholding [1]_is a method for selecting an intensity value
    for thresholding an image into foreground and background. The sel-
    ected intensity threshold maximizes the inter-class variance.

    Parameters
    ----------
        data : numpy.ndarray
            The data to threshold
        bins : Int or numpy.ndarray, optional
            Bin edges, as passed to numpy.histogram

    Returns
    -------
        numpy.float
            The value of the threshold which maximizes the inter-class
            variance.

    Notes
    -----
        This could be generalized to more than 2 classes.
    References
    ----------
        ..[1] N. Otsu, "A Threshold Selection Method from Gray-level
            Histograms," IEEE Trans. Syst., Man, Cybern., Syst., 9, 1,
            62-66 (1979)
    """
    h0, x0 = np.histogram(data.ravel(), bins=bins)
    h = h0.astype('float') / h0.sum()  #normalize
    x = 0.5*(x0[1:] + x0[:-1])  #bin center
    wk = np.array([h[:i+1].sum() for i in range(h.size)])  #omega_k
    mk = np.array([sum(x[:i+1]*h[:i+1]) for i in range(h.size)])  #mu_k
    mt = mk[-1]  #mu_T
    sb = (mt*wk - mk)**2 / (wk*(1-wk) + 1e-15)  #sigma_b
    ind = sb.argmax()
    return 0.5*(x0[ind] + x0[ind+1])