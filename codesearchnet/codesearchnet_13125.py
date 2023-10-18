def _getarray(loci, snames):
    """ 
    parse loci list and return presence/absence matrix
    ordered by the tips on the tree or list of names.
    """
    ## make an empty matrix
    lxs = np.zeros((len(snames), len(loci)), dtype=np.uint64)

    ## fill the matrix
    for loc in xrange(len(loci)):
        for seq in loci[loc].split("\n"):
            if "//" not in seq:
                lxs[snames.index(seq.split()[0][:]), loc] += 1

    return lxs, snames