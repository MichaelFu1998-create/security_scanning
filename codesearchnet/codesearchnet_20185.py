def simplex(x, rho):
    """
    Projection onto the probability simplex

    http://arxiv.org/pdf/1309.1541v1.pdf
    """

    # sort the elements in descending order
    u = np.flipud(np.sort(x.ravel()))
    lambdas = (1 - np.cumsum(u)) / (1. + np.arange(u.size))
    ix = np.where(u + lambdas > 0)[0].max()
    return np.maximum(x + lambdas[ix], 0)