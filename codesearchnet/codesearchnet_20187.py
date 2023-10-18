def fantope(x, rho, dim, tol=1e-4):
    """
    Projection onto the fantope [1]_

    .. [1] Vu, Vincent Q., et al. "Fantope projection and selection: A
           near-optimal convex relaxation of sparse PCA." Advances in
           neural information processing systems. 2013.
    """

    U, V = np.linalg.eigh(x)

    minval, maxval = np.maximum(U.min(), 0), np.maximum(U.max(), 20 * dim)

    while True:

        theta = 0.5 * (maxval + minval)
        thr_eigvals = np.minimum(np.maximum((U - theta), 0), 1)
        constraint = np.sum(thr_eigvals)

        if np.abs(constraint - dim) <= tol:
            break

        elif constraint < dim:
            maxval = theta

        elif constraint > dim:
            minval = theta

        else:
            break

    return np.linalg.multi_dot((V, np.diag(thr_eigvals), V.T))