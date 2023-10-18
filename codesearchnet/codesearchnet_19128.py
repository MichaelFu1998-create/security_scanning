def jensen_shannon(Ks, dim, X_rhos, Y_rhos, required,
                   clamp=True, to_self=False):
    r'''
    Estimate the difference between the Shannon entropy of an equally-weighted
    mixture between X and Y and the mixture of the Shannon entropies:

        JS(X, Y) = H[ (X + Y) / 2 ] - (H[X] + H[Y]) / 2

    We use a special case of the Hino-Murata weighted information estimator with
    a fixed M = n \alpha, about equivalent to the K-nearest-neighbor approach
    used for the other estimators:

        Hideitsu Hino and Noboru Murata (2013).
        Information estimators for weighted observations. Neural Networks.
        http://linkinghub.elsevier.com/retrieve/pii/S0893608013001676


    The estimator for JS(X, Y) is:

        log volume of the unit ball - log M + log(n + m - 1) + digamma(M)
        + 1/2 mean_X( d * log radius of largest ball in X+Y around X_i
                                with no more than M/(n+m-1) weight
                                where X points have weight 1 / (2 n - 1)
                                  and Y points have weight n / (m (2 n - 1))
                      - digamma(# of neighbors in that ball) )
        + 1/2 mean_Y( d * log radius of largest ball in X+Y around Y_i
                                with no more than M/(n+m-1) weight
                                where X points have weight m / (n (2 m - 1))
                                  and Y points have weight 1 / (2 m - 1)
                      - digamma(# of neighbors in that ball) )

        - 1/2 (log volume of the unit ball - log M + log(n - 1) + digamma(M))
        - 1/2 mean_X( d * log radius of the largest ball in X around X_i
                                with no more than M/(n-1) weight
                                where X points have weight 1 / (n - 1))
                      - digamma(# of neighbors in that ball) )

        - 1/2 (log volume of the unit ball - log M + log(m - 1) + digamma(M))
        - 1/2 mean_Y( d * log radius of the largest ball in Y around Y_i
                                with no more than M/(n-1) weight
                                where X points have weight 1 / (m - 1))
                      - digamma(# of neighbors in that ball) )

        =

        log(n + m - 1) + digamma(M)
        + 1/2 mean_X( d * log radius of largest ball in X+Y around X_i
                                with no more than M/(n+m-1) weight
                                where X points have weight 1 / (2 n - 1)
                                  and Y points have weight n / (m (2 n - 1))
                      - digamma(# of neighbors in that ball) )
        + 1/2 mean_Y( d * log radius of largest ball in X+Y around Y_i
                                with no more than M/(n+m-1) weight
                                where X points have weight m / (n (2 m - 1))
                                  and Y points have weight 1 / (2 m - 1)
                      - digamma(# of neighbors in that ball) )
        - 1/2 [log(n-1) + mean_X( d * log rho_M(X_i) )]
        - 1/2 [log(m-1) + mean_Y( d * log rho_M(Y_i) )]
    '''

    X_ns = np.array([rho.shape[0] for rho in X_rhos])
    Y_ns = np.array([rho.shape[0] for rho in Y_rhos])
    n_X = X_ns.size
    n_Y = Y_ns.size

    # cores[0, k, i, j, 0] is mean_X(d * ... - psi(...)) for X[i], Y[j], M=Ks[k]
    # cores[0, k, i, j, 1] is mean_Y(d * ... - psi(...)) for X[i], Y[j], M=Ks[k]
    cores = required
    assert cores.shape == (1, Ks.size, n_X, n_Y, 2)

    # X_bits[k, i] is log(n-1) + mean_X( d * log rho_M(X_i) )  for X[i], M=Ks[k]
    X_bits = np.empty((Ks.size, n_X), dtype=np.float32)
    for i, rho in enumerate(X_rhos):
        X_bits[:, i] = dim * np.mean(np.log(rho), axis=0)
    X_bits += np.log(X_ns - 1)[np.newaxis, :]

    # Y_bits[k, j] is log(n-1) + mean_Y( d * log rho_M(Y_i) )  for Y[j], M=Ks[k]
    Y_bits = np.empty((Ks.size, n_Y), dtype=np.float32)
    for j, rho in enumerate(Y_rhos):
        Y_bits[:, j] = dim * np.mean(np.log(rho), axis=0)
    Y_bits += np.log(Y_ns - 1)[np.newaxis, :]

    est = cores.sum(axis=4)
    est -= X_bits.reshape(1, Ks.size, n_X, 1)
    est -= Y_bits.reshape(1, Ks.size, 1, n_Y)
    est /= 2
    est += np.log(-1 + X_ns[None, None, :, None] + Y_ns[None, None, None, :])
    est += psi(Ks)[None, :, None, None]

    # diagonal is zero
    if to_self:
        est[:, :, xrange(n_X), xrange(n_Y)] = 0

    if clamp:  # know that 0 <= JS <= ln(2)
        np.maximum(0, est, out=est)
        np.minimum(np.log(2), est, out=est)
    return est[:, :, :, :, None]