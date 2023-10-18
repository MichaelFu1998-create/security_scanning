def KIC(N, rho, k):
    r"""Kullback information criterion

    .. math:: KIC(k) = log(\rho_k) + 3 \frac{k+1}{N}

    :validation: double checked versus octave.
    """
    from numpy import log, array
    res = log(rho) + 3. * (k+1.) /float(N)
    return res