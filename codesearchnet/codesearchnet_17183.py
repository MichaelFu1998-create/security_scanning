def _binomial_pmf(n, p):
    """
    Compute the binomial PMF according to Newman and Ziff

    Helper function for :func:`canonical_averages`

    See Also
    --------

    canonical_averages

    Notes
    -----

    See Newman & Ziff, Equation (10) [10]_

    References
    ----------

    .. [10] Newman, M. E. J. & Ziff, R. M. Fast monte carlo algorithm for site
        or bond percolation. Physical Review E 64, 016706+ (2001),
        `doi:10.1103/physreve.64.016706 <http://dx.doi.org/10.1103/physreve.64.016706>`_.

    """

    n = int(n)
    ret = np.empty(n + 1)

    nmax = int(np.round(p * n))

    ret[nmax] = 1.0

    old_settings = np.seterr(under='ignore')  # seterr to known value

    for i in range(nmax + 1, n + 1):
        ret[i] = ret[i - 1] * (n - i + 1.0) / i * p / (1.0 - p)

    for i in range(nmax - 1, -1, -1):
        ret[i] = ret[i + 1] * (i + 1.0) / (n - i) * (1.0 - p) / p

    np.seterr(**old_settings)  # reset to default

    return ret / ret.sum()