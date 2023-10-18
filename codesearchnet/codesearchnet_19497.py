def likelihood_weighting(X, e, bn, N):
    """Estimate the probability distribution of variable X given
    evidence e in BayesNet bn.  [Fig. 14.15]
    >>> seed(1017)
    >>> likelihood_weighting('Burglary', dict(JohnCalls=T, MaryCalls=T),
    ...   burglary, 10000).show_approx()
    'False: 0.702, True: 0.298'
    """
    W = dict((x, 0) for x in bn.variable_values(X))
    for j in xrange(N):
        sample, weight = weighted_sample(bn, e) # boldface x, w in Fig. 14.15
        W[sample[X]] += weight
    return ProbDist(X, W)