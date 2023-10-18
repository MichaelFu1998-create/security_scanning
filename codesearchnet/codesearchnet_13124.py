def share_matrix(locifile, tree=None, nameorder=None):
    """ 
    returns a matrix of shared RAD-seq data 
    
    Parameters:
    -----------
    locifile (str):
        Path to a ipyrad .loci file. 
    tree (str):
        Path to Newick file or a Newick string representation of
        a tree. If used, names will be ordered by the ladderized
        tip order. 
    nameorder (list):
        If a tree is not provided you can alternatively enter 
        the sample order as a list here. The tree argument will
        override this argument.

    Returns:
    --------
    matrix (numpy.array):
        A uint64 numpy array of the number of shared loci between
        all pairs of samples.
    """

    ## load in the loci data
    with open(locifile, 'r') as locidata:
        loci = locidata.read().split("|\n")[:-1]

    ## load in the tree from a string
    if tree:
        tree = ete.Tree(tree)
        tree.ladderize()
        snames = tree.get_leaf_names()
        lxs, names = _getarray(loci, snames)
    elif nameorder:
        lxs, names = _getarray(loci, nameorder)
    else:
        raise IOError("must provide either tree or nameorder argument")

    ## get share matrix
    share = _countmatrix(lxs)

    return share