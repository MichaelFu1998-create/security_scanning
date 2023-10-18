def _get_signif_5(arr, nboots):
    """
    returns a list of stats and an array of dstat boots. Stats includes
    z-score and two-sided P-value. 
    """

    statsarr = np.zeros((3, 7), dtype=np.float64)
    bootsarr = np.zeros((3, nboots))

    idx = 0
    for acol in [2, 3, 4]:
        rows = np.array([0, 1, acol, 5])
        tarr = arr[:, rows, :]

        abxa, baxa, dst = _prop_dstat(tarr)
        boots = _get_boots(tarr, nboots)
        estimate, stddev = (boots.mean(), boots.std())
        if stddev:
            zscore = np.abs(dst) / stddev
        else:
            zscore = np.NaN
        stats = [dst, estimate, stddev, zscore, abxa, baxa, arr.shape[0]]

        statsarr[idx] = stats
        bootsarr[idx] = boots
        idx += 1

    return statsarr, bootsarr