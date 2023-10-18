def AIC(N, rho, k):
    r"""Akaike Information Criterion

    :param rho: rho at order k
    :param N: sample size
    :param k: AR order.

    If k is the AR order and N the size of the sample, then Akaike criterion is

    .. math:: AIC(k) = \log(\rho_k) + 2\frac{k+1}{N}

    ::

        AIC(64, [0.5,0.3,0.2], [1,2,3])

    :validation: double checked versus octave.
    """
    from numpy import log, array
    #k+1 #todo check convention. agrees with octave

    res = N * log(array(rho)) + 2.* (array(k)+1)
    return res