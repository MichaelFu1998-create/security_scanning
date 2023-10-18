def aic_eigen(s, N):
    r"""AIC order-selection using eigen values

    :param s: a list of `p` sorted eigen values
    :param N: the size of the input data. To be defined precisely.

    :return:
        * an array containing the AIC values

    Given :math:`n` sorted eigen values :math:`\lambda_i` with
    :math:`0 <= i < n`, the proposed criterion from Wax and Kailath (1985)
    is:

    .. math:: AIC(k) = -2(n-k)N \ln \frac{g(k)}{a(k)} + 2k(2n-k)

    where the arithmetic sum :math:`a(k)` is:

    .. math:: a(k) = \sum_{i=k+1}^{n}\lambda_i

    and the geometric sum :math:`g(k)` is:

    .. math:: g(k) = \prod_{i=k+1}^{n} \lambda_i^{-(n-k)}

    The number of relevant sinusoids in the signal subspace is determined by
    selecting the minimum of `AIC`.

    .. seealso:: :func:`~spectrum.eigenfreq.eigen`
    .. todo:: define precisely the input parameter N. Should be the input
       data length but when using correlation matrix (SVD), I suspect it
       should be the length of the correlation matrix rather than the
       original data.

    :References:
        * [Marple]_ Chap 13,
        * [Wax]_
    """
    import numpy as np

    kaic = []
    n = len(s)
    for k in range(0, n-1):
        ak = 1./(n-k) * np.sum(s[k+1:])
        gk = np.prod(s[k+1:]**(1./(n-k)))
        kaic.append( -2.*(n-k)*N * np.log(gk/ak) + 2.*k*(2.*n-k))

    return kaic