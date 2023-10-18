def AICc(N, rho, k, norm=True):
    r"""corrected Akaike information criterion

    .. math:: AICc(k) = log(\rho_k) + 2 \frac{k+1}{N-k-2}


    :validation: double checked versus octave.
    """
    from numpy import log, array
    p = k  #todo check convention. agrees with octave
    res = log(rho) + 2. * (p+1) / (N-p-2)
    return res