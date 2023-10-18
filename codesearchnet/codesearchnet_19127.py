def quadratic(Ks, dim, rhos, required=None):
    r'''
    Estimates \int p^2 based on kNN distances.

    In here because it's used in the l2 distance, above.

    Returns array of shape (num_Ks,).
    '''
    # Estimated with alpha=1, beta=0:
    #   B_{k,d,1,0} is the same as B_{k,d,0,1} in linear()
    # and the full estimator is
    #   B / (n - 1) * mean(rho ^ -dim)
    N = rhos.shape[0]
    Ks = np.asarray(Ks)
    Bs = (Ks - 1) / np.pi ** (dim / 2) * gamma(dim / 2 + 1)  # shape (num_Ks,)
    est = Bs / (N - 1) * np.mean(rhos ** (-dim), axis=0)
    return est