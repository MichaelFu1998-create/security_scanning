def _get_signif_4(arr, nboots):
    """
    returns a list of stats and an array of dstat boots. Stats includes
    z-score and two-sided P-value. 
    """
    abba, baba, dst = _prop_dstat(arr)
    boots = _get_boots(arr, nboots)
    estimate, stddev = (boots.mean(), boots.std())
    zscore = 0.
    if stddev:
        zscore = np.abs(dst) / stddev
    stats = [dst, estimate, stddev, zscore, abba, baba, arr.shape[0]]
    return np.array(stats), boots