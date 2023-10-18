def AKICc(N, rho, k):
    r"""approximate corrected Kullback information

    .. math:: AKICc(k) = log(rho_k) + \frac{p}{N*(N-k)} + (3-\frac{k+2}{N})*\frac{k+1}{N-k-2}

    """
    from numpy import log, array
    p = k
    res = log(rho) + p/N/(N-p) + (3.-(p+2.)/N) * (p+1.) / (N-p-2.)
    return res