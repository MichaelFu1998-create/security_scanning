def gibbs_ask(X, e, bn, N):
    """[Fig. 14.16]
    >>> seed(1017)
    >>> gibbs_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary, 1000
    ...  ).show_approx()
    'False: 0.738, True: 0.262'
    """
    assert X not in e, "Query variable must be distinct from evidence"
    counts = dict((x, 0) for x in bn.variable_values(X)) # bold N in Fig. 14.16
    Z = [var for var in bn.vars if var not in e]
    state = dict(e) # boldface x in Fig. 14.16
    for Zi in Z:
        state[Zi] = choice(bn.variable_values(Zi))
    for j in xrange(N):
        for Zi in Z:
            state[Zi] = markov_blanket_sample(Zi, state, bn)
            counts[state[X]] += 1
    return ProbDist(X, counts)