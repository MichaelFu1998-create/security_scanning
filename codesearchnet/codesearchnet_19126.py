def l2(Ks, dim, X_rhos, Y_rhos, required, clamp=True, to_self=False):
    r'''
    Estimates the L2 distance between distributions, via
        \int (p - q)^2 = \int p^2 - \int p q - \int q p + \int q^2.

    \int pq and \int qp are estimated with the linear function (in both
    directions), while \int p^2 and \int q^2 are estimated via the quadratic
    function below.

    Always clamps negative estimates of l2^2 to 0, because otherwise the sqrt
    would break.
    '''
    n_X = len(X_rhos)
    n_Y = len(Y_rhos)

    linears = required
    assert linears.shape == (1, Ks.size, n_X, n_Y, 2)

    X_quadratics = np.empty((Ks.size, n_X), dtype=np.float32)
    for i, rho in enumerate(X_rhos):
        X_quadratics[:, i] = quadratic(Ks, dim, rho)

    Y_quadratics = np.empty((Ks.size, n_Y), dtype=np.float32)
    for j, rho in enumerate(Y_rhos):
        Y_quadratics[:, j] = quadratic(Ks, dim, rho)

    est = -linears.sum(axis=4)
    est += X_quadratics[None, :, :, None]
    est += Y_quadratics[None, :, None, :]
    np.maximum(est, 0, out=est)
    np.sqrt(est, out=est)

    # diagonal is of course known to be zero
    if to_self:
        est[:, :, xrange(n_X), xrange(n_Y)] = 0
    return est[:, :, :, :, None]