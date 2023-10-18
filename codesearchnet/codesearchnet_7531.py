def mdl_eigen(s, N):
    r"""MDL order-selection using eigen values

    :param s: a list of `p` sorted eigen values
    :param N: the size of the input data. To be defined precisely.

    :return:
        * an array containing the AIC values

    .. math:: MDL(k) = (n-k)N \ln \frac{g(k)}{a(k)} + 0.5k(2n-k) log(N)

    .. seealso:: :func:`aic_eigen` for details

    :References:
        * [Marple]_ Chap 13,
        * [Wax]_
    """
    import numpy as np
    kmdl = []
    n = len(s)
    for k in range(0, n-1):
        ak = 1./(n-k) * np.sum(s[k+1:])
        gk = np.prod(s[k+1:]**(1./(n-k)))
        kmdl.append( -(n-k)*N * np.log(gk/ak) + 0.5*k*(2.*n-k)*np.log(N))
    return kmdl