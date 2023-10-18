def maxind_numba(block):
    """ filter for indels """
    ## remove terminal edges
    inds = 0
    for row in xrange(block.shape[0]):
        where = np.where(block[row] != 45)[0]
        if len(where) == 0:
            obs = 100
        else:
            left = np.min(where)
            right = np.max(where)
            obs = np.sum(block[row, left:right] == 45)
        if obs > inds:
            inds = obs
    return inds