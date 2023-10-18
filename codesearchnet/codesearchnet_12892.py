def _countmatrix(lxs):
    """ fill a matrix with pairwise data sharing """
    
    ## an empty matrix
    share = np.zeros((lxs.shape[0], lxs.shape[0]))

    ## fill above
    names = range(lxs.shape[0])
    for row in lxs:
        for samp1, samp2 in itertools.combinations(names, 2):
            shared = lxs[samp1, lxs[samp2] > 0].sum()
            share[samp1, samp2] = shared

    ## mirror below
    ##share[]

    ## fill diagonal with total sample coverage
    for row in xrange(len(names)):
        share[row, row] = lxs[row].sum()

    return share