def count_var(nex):
    """
    count number of sites with cov=4, and number of variable sites.
    """
    arr = np.array([list(i.split()[-1]) for i in nex])
    miss = np.any(arr=="N", axis=0)
    nomiss = arr[:, ~miss]
    nsnps = np.invert(np.all(nomiss==nomiss[0, :], axis=0)).sum()
    return nomiss.shape[1], nsnps