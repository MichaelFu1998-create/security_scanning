def MDL(N, rho, k):
    r"""Minimum Description Length

    .. math:: MDL(k) = N log \rho_k + p \log N

    :validation: results
    """
    from numpy import log
    #p = arange(1, len(rho)+1)
    mdl = N* log(rho) + k * log(N)
    return mdl