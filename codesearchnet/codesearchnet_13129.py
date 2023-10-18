def _get_boots(arr, nboots):
    """
    return array of bootstrap D-stats
    """
    ## hold results (nboots, [dstat, ])
    boots = np.zeros((nboots,))
    
    ## iterate to fill boots
    for bidx in xrange(nboots):
        ## sample with replacement
        lidx = np.random.randint(0, arr.shape[0], arr.shape[0])
        tarr = arr[lidx]
        _, _, dst = _prop_dstat(tarr)
        boots[bidx] = dst
    
    ## return bootarr
    return boots