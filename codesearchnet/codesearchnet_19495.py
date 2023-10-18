def rejection_sampling(X, e, bn, N):
    """Estimate the probability distribution of variable X given
    evidence e in BayesNet bn, using N samples.  [Fig. 14.14]
    Raises a ZeroDivisionError if all the N samples are rejected,
    i.e., inconsistent with e.
    >>> seed(47)
    >>> rejection_sampling('Burglary', dict(JohnCalls=T, MaryCalls=T),
    ...   burglary, 10000).show_approx()
    'False: 0.7, True: 0.3'
    """
    counts = dict((x, 0) for x in bn.variable_values(X)) # bold N in Fig. 14.14
    for j in xrange(N):
        sample = prior_sample(bn) # boldface x in Fig. 14.14
        if consistent_with(sample, e):
            counts[sample[X]] += 1
    return ProbDist(X, counts)