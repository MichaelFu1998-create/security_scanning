def FPE(N,rho, k=None):
    r"""Final prediction error criterion

    .. math:: FPE(k) = \frac{N + k + 1}{N - k - 1} \rho_k

    :validation: double checked versus octave.

    """
    #k #todo check convention. agrees with octave
    fpe = rho * (N + k + 1.) / (N- k -1)
    return fpe