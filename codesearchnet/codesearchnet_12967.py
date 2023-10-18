def consensus_tree(trees, names=None, cutoff=0.0):
    """ 
    An extended majority rule consensus function for ete3. 
    Modelled on the similar function from scikit-bio tree module. If 
    cutoff=0.5 then it is a normal majority rule consensus, while if 
    cutoff=0.0 then subsequent non-conflicting clades are added to the tree.
    """

    ## find which clades occured with freq > cutoff
    namedict, clade_counts = _find_clades(trees, names=names)

    ## filter out the < cutoff clades
    fclade_counts = _filter_clades(clade_counts, cutoff)

    ## build tree
    consens_tree, _ = _build_trees(fclade_counts, namedict)
    ## make sure no singleton nodes were left behind
    return consens_tree, clade_counts