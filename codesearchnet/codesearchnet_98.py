def compute_geometric_median(X, eps=1e-5):
    """
    Estimate the geometric median of points in 2D.

    Code from https://stackoverflow.com/a/30305181

    Parameters
    ----------
    X : (N,2) ndarray
        Points in 2D. Second axis must be given in xy-form.

    eps : float, optional
        Distance threshold when to return the median.

    Returns
    -------
    (2,) ndarray
        Geometric median as xy-coordinate.

    """
    y = np.mean(X, 0)

    while True:
        D = scipy.spatial.distance.cdist(X, [y])
        nonzeros = (D != 0)[:, 0]

        Dinv = 1 / D[nonzeros]
        Dinvs = np.sum(Dinv)
        W = Dinv / Dinvs
        T = np.sum(W * X[nonzeros], 0)

        num_zeros = len(X) - np.sum(nonzeros)
        if num_zeros == 0:
            y1 = T
        elif num_zeros == len(X):
            return y
        else:
            R = (T - y) * Dinvs
            r = np.linalg.norm(R)
            rinv = 0 if r == 0 else num_zeros/r
            y1 = max(0, 1-rinv)*T + min(1, rinv)*y

        if scipy.spatial.distance.euclidean(y, y1) < eps:
            return y1

        y = y1