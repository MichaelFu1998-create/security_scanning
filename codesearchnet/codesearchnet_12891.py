def _getarray(loci, tree):
    """ 
    parse the loci file list and return presence/absence matrix
    ordered by the tips on the tree
    """

    ## order tips
    tree.ladderize()

    ## get tip names
    snames = tree.get_leaf_names()

    ## make an empty matrix
    lxs = np.zeros((len(snames), len(loci)), dtype=np.int)

    ## fill the matrix
    for loc in xrange(len(loci)):
        for seq in loci[loc].split("\n")[:-1]:
            lxs[snames.index(seq.split()[0]), loc] += 1

    return lxs, snames