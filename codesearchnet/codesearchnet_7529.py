def CAT(N, rho, k):
    r"""Criterion Autoregressive Transfer Function :

    .. math::  CAT(k) = \frac{1}{N} \sum_{i=1}^k \frac{1}{\rho_i} - \frac{\rho_i}{\rho_k}

    .. todo:: validation
    """
    from numpy import zeros, arange
    cat = zeros(len(rho))
    for p in arange(1, len(rho)+1):
        rho_p = float(N)/(N-p)*rho[p-1]
        s = 0
        for j in range(1, p+1):
            rho_j = float(N)/(N-j)*rho[j-1]
            s = s + 1./rho_j
        #print(s, s/float(N), 1./rho_p)
        cat[p-1] = s/float(N) - 1./rho_p
    return cat