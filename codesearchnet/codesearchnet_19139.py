def kl(Ks, dim, num_q, rhos, nus, clamp=True):
    r'''
    Estimate the KL divergence between distributions:
        \int p(x) \log (p(x) / q(x))
    using the kNN-based estimator (5) of
        Qing Wang, Sanjeev R Kulkarni, and Sergio Verdu (2009).
        Divergence Estimation for Multidimensional Densities Via
        k-Nearest-Neighbor Distances.
        IEEE Transactions on Information Theory.
        http://www.ee.princeton.edu/~verdu/reprints/WanKulVer.May2009.pdf
    which is:
        d * 1/n \sum \log (nu_k(i) / rho_k(i)) + log(m / (n - 1))

    If clamp, enforces KL >= 0.

    Returns an array of shape (num_Ks,).
    '''
    est = dim * np.mean(np.log(nus) - np.log(rhos), axis=0)
    est += np.log(num_q / (rhos.shape[0] - 1))
    if clamp:
        np.maximum(est, 0, out=est)
    return est