def gmm_cause(points, k=4, p1=2, p2=2):
    """Init a root cause with a Gaussian Mixture Model w/ a spherical covariance type."""
    g = GMM(k, covariance_type="spherical")
    g.fit(np.random.randn(300, 1))

    g.means_ = p1 * np.random.randn(k, 1)
    g.covars_ = np.power(abs(p2 * np.random.randn(k, 1) + 1), 2)
    g.weights_ = abs(np.random.rand(k))
    g.weights_ = g.weights_ / sum(g.weights_)
    return g.sample(points)[0].reshape(-1)